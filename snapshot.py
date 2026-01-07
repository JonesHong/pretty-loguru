#!/usr/bin/env python3
"""
snapshot.py
----------------
這是一個「單檔、零依賴（僅標準庫）」的專案快照工具，用於快速產出：
1) 專案目錄樹（ASCII tree）
2) Python AST 符號清單（function / class / method，支援巢狀結構）
3) 依賴清單摘要（pyproject.toml / requirements*.txt / Pipfile）

設計目標（務實、可維護、可擴充）：
- 以 dataclass 集中管理設定（Config）
- 以類別封裝責任（Scanner / Analyzer / DependencyParser / ReportGenerator）
- AST 解析使用 ast.NodeVisitor（可處理巢狀定義）
- 支援 .gitignore（包含子目錄的 .gitignore），並與額外排除規則共存
- 維持輸出穩定（排序固定），方便 diff / code review

使用方式：
    python snapshot.py --help

最常見：在專案根目錄執行並輸出 snapshot.md
    python snapshot.py
"""

from __future__ import annotations

import ast
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

try:
    # Python 3.11+：tomllib 是標準庫（仍屬於「零依賴」）
    import tomllib  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


# =============================================================================
# 預設排除與依賴檔案型態
# =============================================================================
DEFAULT_EXCLUDES: Tuple[str, ...] = (
    # VCS / cache / build / env
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    ".eggs",
    "*.egg-info",
    "node_modules",
    "site-packages",
    ".DS_Store",
    ".vscode",
    ".idea",
    ".benchmarks",
    # 常見「非核心」資料夾（預設排除避免輸出爆長）
    "backups",
    "templates",
    "references",
    "examples",
    "scripts",
    "tests",
    "snapshot_v2.py",
)

DEPENDENCY_MANIFEST_GLOBS: Tuple[str, ...] = (
    "pyproject.toml",
    "Pipfile",
    "requirements*.txt",
)


# =============================================================================
# 資料結構
# =============================================================================
@dataclass(frozen=True)
class SymbolSnapshot:
    """單一 Python 符號快照（class/function/method 或 error）。"""
    kind: str  # "function" | "method" | "class" | "error"
    name: str  # qualified name（含巢狀路徑，例如 Outer.inner / A.B.method）
    signature: str
    doc: str
    lineno: int


@dataclass(frozen=True)
class FileSnapshot:
    """單一檔案的符號清單快照。"""
    path: str
    symbols: List[SymbolSnapshot]


@dataclass(frozen=True)
class ProjectDeps:
    """單一依賴清單檔案（pyproject/requirements...）解析結果。"""
    project_path: str
    project_name: str
    dependencies: Dict[str, str]
    dev_dependencies: Dict[str, str]
    source: str


@dataclass(frozen=True)
class Config:
    """
    Snapshot 工具設定。

    設計原則：
    - 將「可調參數」集中在一個物件內，避免全域變數散落。
    - 預設值偏保守：避免不小心掃到超大資料夾、或解析巨型檔案造成卡住。
    """

    root: Path
    output: Path

    max_tree_depth: int = 12
    include_private_symbols: bool = True
    include_nested_symbols: bool = False
    follow_symlinks: bool = False
    use_gitignore: bool = True
    use_default_excludes: bool = True
    extra_excludes: Tuple[str, ...] = ()

    # 單檔最大解析大小（避免誤把大型資料檔當作 .py）
    max_file_bytes: int = 1_000_000

    # AST 分析目標副檔名（目錄樹不受此限制）
    target_exts: Tuple[str, ...] = (".py",)


# =============================================================================
# .gitignore（零依賴版）
# =============================================================================
@dataclass(frozen=True)
class _GitIgnoreRule:
    """
    一條 .gitignore 規則（簡化實作）。

    支援的子集合（常見且高價值）：
    - 空行 / # 註解
    - `!` 反向規則（unignore）
    - `/` 開頭：以該 .gitignore 所在目錄作為錨點（anchored）
    - `/` 結尾：只針對目錄（並排除其子樹）
    - glob：`* ? []` 與常見 `**`

    不追求完整 gitignore 規格（那會變成另一個專案），目標是「夠用且可讀」。
    """

    base_dir: str  # 相對於 root 的 posix path（.gitignore 所在目錄）
    pattern: str
    negated: bool
    dir_only: bool
    anchored: bool


class GitIgnore:
    """
    讀取並套用 .gitignore 規則。

    重要行為：
    - 同一路徑可能同時命中多條規則；採「最後命中者生效」。
    - 每個 .gitignore 的規則只影響其所在目錄（base_dir）之下的路徑。
    """

    def __init__(self, root: Path, *, follow_symlinks: bool) -> None:
        """建立 .gitignore 規則集合（需呼叫 `load()` 才會讀取檔案）。"""
        self._root = root
        self._follow_symlinks = follow_symlinks
        self._rules: List[_GitIgnoreRule] = []

    def load(self) -> None:
        """走訪專案並讀取所有 `.gitignore`，建構規則清單。"""
        self._rules.clear()
        for gi in self._iter_gitignore_files():
            base_dir = self._to_posix_rel(gi.parent)
            self._rules.extend(self._parse_gitignore_file(gi, base_dir=base_dir))

    def is_ignored(self, path: Path) -> bool:
        """判斷給定路徑是否被 .gitignore 規則排除。"""
        rel_posix = self._to_posix_rel(path)
        if rel_posix == ".":
            return False

        ignored: Optional[bool] = None
        for rule in self._rules:
            if not self._rule_matches(rule, rel_posix):
                continue
            ignored = not rule.negated
        return bool(ignored)

    def _iter_gitignore_files(self) -> Iterator[Path]:
        """列出專案內所有 `.gitignore` 檔案（依 os.walk 掃描）。"""
        for dirpath, dirnames, filenames in os.walk(self._root, followlinks=self._follow_symlinks):
            # 即便使用者關閉 default excludes，也先硬排除 VCS 目錄以避免掃描成本爆炸
            dirnames[:] = [d for d in dirnames if d not in (".git", ".hg", ".svn")]
            if ".gitignore" in filenames:
                yield Path(dirpath) / ".gitignore"

    def _parse_gitignore_file(self, path: Path, *, base_dir: str) -> List[_GitIgnoreRule]:
        """解析單一 `.gitignore` 檔案為規則清單。"""
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return []

        rules: List[_GitIgnoreRule] = []
        for raw_line in text.splitlines():
            line = raw_line.rstrip("\n\r")
            if not line.strip():
                continue
            if line.lstrip().startswith("#"):
                continue

            negated = line.startswith("!")
            if negated:
                line = line[1:]

            line = line.strip()
            if not line:
                continue

            dir_only = line.endswith("/")
            if dir_only:
                line = line[:-1]

            anchored = line.startswith("/")
            if anchored:
                line = line.lstrip("/")

            rules.append(
                _GitIgnoreRule(
                    base_dir=base_dir,
                    pattern=line,
                    negated=negated,
                    dir_only=dir_only,
                    anchored=anchored,
                )
            )
        return rules

    def _rule_matches(self, rule: _GitIgnoreRule, rel_posix: str) -> bool:
        """判斷某條規則是否命中 `rel_posix`（posix 相對路徑）。"""
        # 1) base_dir 作用域
        scoped_rel = rel_posix
        if rule.base_dir and rule.base_dir != ".":
            prefix = rule.base_dir.rstrip("/") + "/"
            if rel_posix != rule.base_dir and not rel_posix.startswith(prefix):
                return False
            scoped_rel = rel_posix[len(prefix) :] if rel_posix.startswith(prefix) else ""

        pat = rule.pattern

        # 2) dir_only：命中資料夾本身或其子樹
        if rule.dir_only:
            if not pat:
                return False
            if scoped_rel == pat or scoped_rel.startswith(pat.rstrip("/") + "/"):
                return True
            first = scoped_rel.split("/", 1)[0] if scoped_rel else ""
            return bool(first and fnmatch.fnmatchcase(first, pat))

        # 3) anchored：從 scoped_rel 開頭比對（不補 **/）
        if rule.anchored:
            if "/" in pat:
                return fnmatch.fnmatchcase(scoped_rel, pat)
            return fnmatch.fnmatchcase(scoped_rel.split("/")[-1], pat)

        # 4) 非 anchored：
        # - pattern 含 /：允許命中任意層級，因此補上一個 **/ 前綴
        # - pattern 不含 /：只比對 basename
        if "/" in pat:
            return fnmatch.fnmatchcase(scoped_rel, pat) or fnmatch.fnmatchcase(scoped_rel, f"**/{pat}")
        return fnmatch.fnmatchcase(scoped_rel.split("/")[-1], pat)

    def _to_posix_rel(self, path: Path) -> str:
        """將任意路徑轉換為相對於 root 的 posix path（用於比對）。"""
        rel = os.path.relpath(path, self._root)
        if rel == ".":
            return "."
        return rel.replace("\\", "/")


# =============================================================================
# 專案掃描
# =============================================================================
class ProjectScanner:
    """
    專案掃描器：負責
    - 走訪目錄
    - 排除規則（default excludes + extra excludes + .gitignore）
    - 產出目錄樹

    這個類別刻意「不做」AST/依賴解析，避免責任混雜。
    """

    def __init__(self, config: Config) -> None:
        """建立掃描器並初始化排除規則（含 .gitignore）。"""
        self._config = config

        excludes = list(DEFAULT_EXCLUDES if config.use_default_excludes else ())
        excludes.extend(config.extra_excludes)
        self._excludes: Tuple[str, ...] = tuple(excludes)

        self._gitignore = (
            GitIgnore(config.root, follow_symlinks=config.follow_symlinks) if config.use_gitignore else None
        )
        if self._gitignore is not None:
            self._gitignore.load()

    def iter_included_files(self) -> Iterator[Path]:
        """走訪 root 並回傳「未被排除」的檔案路徑。"""
        for dirpath, dirnames, filenames in os.walk(self._config.root, followlinks=self._config.follow_symlinks):
            dirnames[:] = [d for d in dirnames if not self._is_excluded(Path(dirpath) / d, is_dir=True)]
            for fn in filenames:
                p = Path(dirpath) / fn
                if self._is_excluded(p, is_dir=False):
                    continue
                yield p

    def iter_python_files(self) -> Iterator[Path]:
        """列出要進行 AST 解析的 Python 檔案（依 `target_exts`）。"""
        exts = {e.lower() for e in self._config.target_exts}
        for p in self.iter_included_files():
            if p.suffix.lower() in exts:
                yield p

    def iter_dependency_manifests(self) -> Iterator[Path]:
        """列出依賴檔案（pyproject/requirements...）供後續解析。"""
        for p in self.iter_included_files():
            if any(fnmatch.fnmatchcase(p.name, g) for g in DEPENDENCY_MANIFEST_GLOBS):
                yield p

    def build_tree(self) -> str:
        """產出專案目錄樹（ASCII tree）。"""
        root_name = f"{self._config.root.name}/"
        lines = [root_name]
        lines.extend(self._build_tree_lines(self._config.root, prefix="", depth=0))
        return "\n".join(lines).rstrip() + "\n"

    def _build_tree_lines(self, dir_path: Path, *, prefix: str, depth: int) -> List[str]:
        """遞迴生成目錄樹的每一行（內部用）。"""
        if depth >= self._config.max_tree_depth:
            return [f"{prefix}└── …"]

        try:
            entries = list(dir_path.iterdir())
        except Exception:
            return [f"{prefix}└── [無法讀取]"]

        visible: List[Path] = []
        for p in entries:
            if p.name in (".", ".."):
                continue
            if self._is_excluded(p, is_dir=p.is_dir()):
                continue
            visible.append(p)

        visible.sort(key=lambda p: (not p.is_dir(), p.name.lower()))

        lines: List[str] = []
        for idx, p in enumerate(visible):
            is_last = idx == len(visible) - 1
            branch = "└── " if is_last else "├── "
            lines.append(f"{prefix}{branch}{p.name}{'/' if p.is_dir() else ''}")
            if p.is_dir():
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(self._build_tree_lines(p, prefix=child_prefix, depth=depth + 1))
        return lines

    def _is_excluded(self, path: Path, *, is_dir: bool) -> bool:
        """判斷路徑是否應被排除（.gitignore + excludes）。"""
        if self._gitignore is not None and self._gitignore.is_ignored(path):
            return True

        rel_posix = os.path.relpath(path, self._config.root).replace("\\", "/")
        parts = [p for p in rel_posix.split("/") if p and p != "."]

        for pat in self._excludes:
            pat_norm = pat.replace("\\", "/").strip()
            if not pat_norm:
                continue

            has_glob = any(ch in pat_norm for ch in ("*", "?", "["))
            if has_glob:
                if fnmatch.fnmatchcase(rel_posix, pat_norm):
                    return True
                if any(fnmatch.fnmatchcase(seg, pat_norm) for seg in parts):
                    return True
            else:
                if pat_norm in parts:
                    return True
                if is_dir and path.name == pat_norm:
                    return True

        return False


# =============================================================================
# AST 解析：NodeVisitor
# =============================================================================
class CodeAnalyzer(ast.NodeVisitor):
    """
    Python AST 分析器：蒐集 function/class/method（含巢狀）。
    """

    def __init__(self, *, include_private: bool, include_nested: bool) -> None:
        """建立 AST analyzer。"""
        self._include_private = include_private
        self._include_nested = include_nested
        self._scope: List[Tuple[str, str]] = []
        self.symbols: List[SymbolSnapshot] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        """拜訪 class 節點並記錄 SymbolSnapshot（符合篩選條件時）。"""
        # 預設只列出 module-level 的 class；避免把 function 內的 inner class 也塞進快照，造成噪音。
        if not self._include_nested and self._in_function_scope():
            self._scope.append(("class", node.name))
            self.generic_visit(node)
            self._scope.pop()
            return

        if self._should_keep(node.name):
            self.symbols.append(
                SymbolSnapshot(
                    kind="class",
                    name=self._qualified(node.name),
                    signature=self._format_class_signature(node),
                    doc=_first_doc_line(ast.get_docstring(node) or ""),
                    lineno=getattr(node, "lineno", 0) or 0,
                )
            )

        self._scope.append(("class", node.name))
        self.generic_visit(node)
        self._scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """拜訪同步 function 節點。"""
        self._handle_function_like(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        """拜訪 async function 節點。"""
        self._handle_function_like(node)

    def _handle_function_like(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """處理 function/method 節點並記錄 SymbolSnapshot（符合篩選條件時）。"""
        # 預設只列出 module-level function 與 class methods；避免把 function 內部的 helper def 也列進快照。
        # 這樣 snapshot.md 更接近「對外 API / 合約」，也能降低「缺少 docstring」的誤判。
        if not self._include_nested and self._in_function_scope():
            self._scope.append(("function", node.name))
            self.generic_visit(node)
            self._scope.pop()
            return

        if self._should_keep(node.name):
            kind = "method" if (self._scope and self._scope[-1][0] == "class") else "function"
            self.symbols.append(
                SymbolSnapshot(
                    kind=kind,
                    name=self._qualified(node.name),
                    signature=self._format_function_signature(node),
                    doc=_first_doc_line(ast.get_docstring(node) or ""),
                    lineno=getattr(node, "lineno", 0) or 0,
                )
            )

        self._scope.append(("function", node.name))
        self.generic_visit(node)
        self._scope.pop()

    def _should_keep(self, name: str) -> bool:
        """依 include_private 設定決定是否保留該 symbol。"""
        return self._include_private or not name.startswith("_")

    def _in_function_scope(self) -> bool:
        """是否目前位於 function scope（用於判斷 nested）。"""
        return any(k == "function" for (k, _n) in self._scope)

    def _qualified(self, name: str) -> str:
        """產生 qualified name（依目前 scope 堆疊）。"""
        if not self._scope:
            return name
        parents = [n for (_k, n) in self._scope if n]
        return ".".join([*parents, name])

    def _format_class_signature(self, node: ast.ClassDef) -> str:
        """輸出 class bases 的簡化表示（避免噴出完整 AST）。"""
        if not node.bases:
            return ""
        bases = [_safe_expr_placeholder(b) for b in node.bases]
        return f"({', '.join(bases)})"

    def _format_function_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """輸出 function signature 的簡化表示（以 `...` 取代型別/預設值）。"""
        args = node.args
        chunks: List[str] = []

        def fmt_arg(a: ast.arg, *, default: bool, annotated: bool) -> str:
            out = a.arg
            if annotated and a.annotation is not None:
                out += ": ..."
            if default:
                out += "=..."
            return out

        posonly = list(args.posonlyargs or [])
        regular = list(args.args or [])
        total_pos = posonly + regular

        defaults = list(args.defaults or [])
        default_flags = [False] * max(0, len(total_pos) - len(defaults)) + [True] * len(defaults)
        for a, has_default in zip(total_pos, default_flags):
            chunks.append(fmt_arg(a, default=has_default, annotated=True))

        if posonly:
            chunks.insert(len(posonly), "/")

        if args.vararg is not None:
            chunks.append("*" + fmt_arg(args.vararg, default=False, annotated=True))
        elif args.kwonlyargs:
            chunks.append("*")

        for kwarg, kw_default in zip(args.kwonlyargs or [], args.kw_defaults or []):
            chunks.append(fmt_arg(kwarg, default=(kw_default is not None), annotated=True))

        if args.kwarg is not None:
            chunks.append("**" + fmt_arg(args.kwarg, default=False, annotated=True))

        sig = "(" + ", ".join(chunks) + ")"
        if node.returns is not None:
            sig += " -> ..."
        return sig


def _first_doc_line(doc: str) -> str:
    """取 docstring 的第一行（用於 snapshot.md 摘要）。"""
    doc = (doc or "").strip()
    if not doc:
        return ""
    return doc.splitlines()[0].strip()


def _safe_expr_placeholder(expr: ast.AST) -> str:
    """將 AST 表達式轉成可讀的簡化佔位字串（失敗則回傳 `...`）。"""
    try:
        if isinstance(expr, ast.Name):
            return expr.id
        if isinstance(expr, ast.Attribute):
            return f"{_safe_expr_placeholder(expr.value)}.{expr.attr}"
        if isinstance(expr, ast.Subscript):
            return f"{_safe_expr_placeholder(expr.value)}[...]"
        if isinstance(expr, ast.Call):
            return f"{_safe_expr_placeholder(expr.func)}(...)"
    except Exception:
        return "..."
    return "..."


class PythonFileParser:
    """解析單一 Python 檔案並產生 `FileSnapshot`（AST symbols）。"""
    def __init__(self, config: Config) -> None:
        """建立 parser。"""
        self._config = config

    def parse(self, path: Path) -> FileSnapshot:
        """解析指定 Python 檔案（包含容錯讀檔/容錯解析）。"""
        rel = os.path.relpath(path, self._config.root).replace("\\", "/")

        try:
            if path.stat().st_size > self._config.max_file_bytes:
                return FileSnapshot(
                    path=rel,
                    symbols=[
                        SymbolSnapshot(
                            kind="error",
                            name="檔案過大",
                            signature="",
                            doc=f"跳過解析：>{self._config.max_file_bytes} bytes",
                            lineno=0,
                        )
                    ],
                )
        except Exception:
            pass

        try:
            # 容忍 UTF-8 BOM（避免 BOM 造成 ast.parse 出現 U+FEFF SyntaxError）。
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            try:
                text = path.read_text(encoding="cp950")
            except Exception as exc:
                return FileSnapshot(
                    path=rel,
                    symbols=[SymbolSnapshot(kind="error", name="讀檔失敗", signature="", doc=str(exc), lineno=0)],
                )
        except Exception as exc:
            return FileSnapshot(
                path=rel,
                symbols=[SymbolSnapshot(kind="error", name="讀檔失敗", signature="", doc=str(exc), lineno=0)],
            )

        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            msg = f"{exc.msg} (line {exc.lineno})"
            return FileSnapshot(
                path=rel,
                symbols=[SymbolSnapshot(kind="error", name="SyntaxError", signature="", doc=msg, lineno=exc.lineno or 0)],
            )
        except Exception as exc:
            return FileSnapshot(
                path=rel,
                symbols=[SymbolSnapshot(kind="error", name="ParseError", signature="", doc=str(exc), lineno=0)],
            )

        analyzer = CodeAnalyzer(
            include_private=self._config.include_private_symbols,
            include_nested=self._config.include_nested_symbols,
        )
        analyzer.visit(tree)
        symbols = sorted(analyzer.symbols, key=lambda s: (s.lineno, s.kind, s.name))
        return FileSnapshot(path=rel, symbols=symbols)


class DependencyParser:
    """解析依賴清單檔案（pyproject/Pipfile/requirements）。"""
    def parse_manifest(self, path: Path, *, root: Path) -> Optional[ProjectDeps]:
        """解析單一 manifest 檔案並回傳 `ProjectDeps`（無法解析則回傳 None）。"""
        rel_dir = os.path.relpath(path.parent, root).replace("\\", "/")
        rel_dir = "." if rel_dir in ("", ".") else rel_dir

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return None

        if path.name == "pyproject.toml":
            deps, dev_deps, name = self._parse_pyproject(text, fallback_name=path.parent.name)
            return ProjectDeps(rel_dir, name, deps, dev_deps, "pyproject.toml")
        if path.name == "Pipfile":
            deps = self._parse_pipfile_section(text, section="packages")
            dev = self._parse_pipfile_section(text, section="dev-packages")
            return ProjectDeps(rel_dir, path.parent.name, deps, dev, "Pipfile")
        if fnmatch.fnmatchcase(path.name, "requirements*.txt"):
            deps = self._parse_requirements(text)
            return ProjectDeps(rel_dir, path.parent.name, deps, {}, path.name)

        return None

    def _parse_requirements(self, text: str) -> Dict[str, str]:
        """解析 requirements.txt 形式的依賴清單。"""
        out: Dict[str, str] = {}
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith(("-", "--")):
                continue
            if " #" in s:
                s = s.split(" #", 1)[0].strip()
            name, spec = _split_dep_name_spec(s)
            if name:
                out[name] = spec
        return out

    def _parse_pyproject(self, text: str, *, fallback_name: str) -> Tuple[Dict[str, str], Dict[str, str], str]:
        """解析 pyproject.toml（優先用 tomllib，失敗則用弱解析）。"""
        if tomllib is not None:
            try:
                data = tomllib.loads(text)  # type: ignore[union-attr]
                return _parse_pyproject_from_toml_dict(data, fallback_name=fallback_name)
            except Exception:
                pass

        name = _weak_toml_get_scalar(text, "project", "name") or fallback_name
        deps = _weak_toml_get_array(text, "project", "dependencies")
        optional = _weak_toml_get_table_of_arrays(text, "project.optional-dependencies")
        dep_groups = _weak_toml_get_table_of_arrays(text, "dependency-groups")

        dependencies = {n: spec for (n, spec) in (_split_dep_name_spec(x) for x in deps) if n}
        dev_dependencies: Dict[str, str] = {}

        for group in ("dev", "development"):
            for entry in optional.get(group, []):
                n, spec = _split_dep_name_spec(entry)
                if n:
                    dev_dependencies[n] = spec
            for entry in dep_groups.get(group, []):
                n, spec = _split_dep_name_spec(entry)
                if n:
                    dev_dependencies[n] = spec

        return dependencies, dev_dependencies, name

    def _parse_pipfile_section(self, text: str, *, section: str) -> Dict[str, str]:
        """解析 Pipfile 的指定 section（packages / dev-packages）。"""
        table = _weak_extract_toml_table(text, section)
        out: Dict[str, str] = {}
        if not table:
            return out
        for line in table.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            m = re.match(r'^([A-Za-z0-9_.\-]+)\s*=\s*["\']?([^"\']+)["\']?\s*$', s)
            if not m:
                continue
            out[m.group(1).strip().lower()] = m.group(2).strip()
        return out


def _split_dep_name_spec(entry: str) -> Tuple[str, str]:
    """將依賴項目字串切成（name, spec）兩段（spec 可為空）。"""
    s = (entry or "").strip()
    if not s:
        return "", ""
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9_.\-]*)(\[[^\]]+\])?\s*(.*)$", s)
    if not m:
        return "", s
    name = m.group(1).strip().lower()
    tail = (m.group(3) or "").strip()
    return name, tail


def _parse_pyproject_from_toml_dict(data: dict, *, fallback_name: str) -> Tuple[Dict[str, str], Dict[str, str], str]:
    """從 `tomllib.loads()` 的結果中萃取 dependencies / dev deps / project name。"""
    name = fallback_name
    dependencies: Dict[str, str] = {}
    dev_dependencies: Dict[str, str] = {}

    project = data.get("project") if isinstance(data, dict) else None
    if isinstance(project, dict):
        name = str(project.get("name") or name)
        for entry in project.get("dependencies") or []:
            if not isinstance(entry, str):
                continue
            n, spec = _split_dep_name_spec(entry)
            if n:
                dependencies[n] = spec

        opt = project.get("optional-dependencies")
        if isinstance(opt, dict):
            for group in ("dev", "development"):
                entries = opt.get(group)
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if not isinstance(entry, str):
                        continue
                    n, spec = _split_dep_name_spec(entry)
                    if n:
                        dev_dependencies[n] = spec

    dep_groups = data.get("dependency-groups")
    if isinstance(dep_groups, dict):
        for group in ("dev", "development"):
            entries = dep_groups.get(group)
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, str):
                    continue
                n, spec = _split_dep_name_spec(entry)
                if n:
                    dev_dependencies[n] = spec

    return dependencies, dev_dependencies, name


def _weak_extract_toml_table(text: str, table: str) -> str:
    """弱解析：擷取 `[table]` 區塊（不完整 TOML 支援，但夠用）。"""
    pattern = re.compile(rf"^\[{re.escape(table)}\]\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    tail = text[start:]
    nxt = re.search(r"^\[[^\]]+\]\s*$", tail, re.MULTILINE)
    end = start + (nxt.start() if nxt else len(tail))
    return text[start:end].strip("\n\r")


def _weak_toml_get_scalar(text: str, table: str, key: str) -> str:
    """弱解析：從 `[table]` 中抓取 scalar 值（字串/數字都以字串回傳）。"""
    block = _weak_extract_toml_table(text, table)
    if not block:
        return ""
    m = re.search(rf"^\s*{re.escape(key)}\s*=\s*(.+)\s*$", block, re.MULTILINE)
    if not m:
        return ""
    raw = m.group(1).strip()
    return raw.strip().strip('"').strip("'")


def _weak_toml_get_array(text: str, table: str, key: str) -> List[str]:
    """弱解析：從 `[table]` 中抓取 string array（`key = ['a','b']`）。"""
    block = _weak_extract_toml_table(text, table)
    if not block:
        return []
    m = re.search(rf"^\s*{re.escape(key)}\s*=\s*\[(.*?)\]\s*$", block, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    inner = m.group(1)
    items = re.findall(r"['\"]([^'\"]+)['\"]", inner)
    return [x.strip() for x in items if x.strip()]


def _weak_toml_get_table_of_arrays(text: str, table: str) -> Dict[str, List[str]]:
    """弱解析：從 `[table]` 中抓取 `key = [..]` 的 table-of-arrays。"""
    block = _weak_extract_toml_table(text, table)
    if not block:
        return {}
    out: Dict[str, List[str]] = {}
    for m in re.finditer(r"^\s*([A-Za-z0-9_.\-]+)\s*=\s*\[(.*?)\]\s*$", block, re.MULTILINE | re.DOTALL):
        key = m.group(1).strip()
        inner = m.group(2)
        items = re.findall(r"['\"]([^'\"]+)['\"]", inner)
        out[key] = [x.strip() for x in items if x.strip()]
    return out


class ReportGenerator:
    """將掃描結果轉成 Markdown 報告。"""
    def to_markdown(
        self,
        *,
        config: Config,
        tree: str,
        file_snaps: List[FileSnapshot],
        deps: List[ProjectDeps],
    ) -> str:
        """產出 snapshot.md 內容。"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines: List[str] = []
        lines.append("# Snapshot")
        lines.append("")
        root_value = config.root.resolve()
        root_display = root_value.as_posix() if hasattr(root_value, "as_posix") else str(root_value)
        lines.append(f"- Root: `{root_display}`")
        lines.append(f"- Generated: `{now}`")
        lines.append(f"- Max tree depth: `{config.max_tree_depth}`")
        lines.append(f"- Include private symbols: `{config.include_private_symbols}`")
        lines.append(f"- Include nested symbols: `{config.include_nested_symbols}`")
        lines.append(f"- Use .gitignore: `{config.use_gitignore}`")
        lines.append("")

        lines.append("## 專案目錄結構")
        lines.append("```text")
        lines.append(tree.rstrip("\n"))
        lines.append("```")
        lines.append("")

        lines.append("## 函式/類別清單（AST）")
        if not file_snaps:
            lines.append("_未找到任何符合條件的 Python 檔案。_")
            lines.append("")
        else:
            for fs in sorted(file_snaps, key=lambda x: x.path):
                if not fs.symbols:
                    continue
                lines.append(f"### `{fs.path}`")
                for s in fs.symbols:
                    doc = f" — {s.doc}" if s.doc else ""
                    if s.kind == "class":
                        lines.append(f"- **class** `{s.name}{s.signature}`{doc}")
                    elif s.kind == "error":
                        lines.append(f"- ⚠️ **{s.name}** {s.doc}")
                    else:
                        lines.append(f"- **{s.kind}** `{s.name}{s.signature}`{doc}")
                lines.append("")

        lines.append("## 依賴清單")
        if not deps:
            lines.append("_未找到依賴清單檔案（pyproject.toml / requirements*.txt / Pipfile）。_")
            lines.append("")
        else:
            for d in sorted(deps, key=lambda x: (x.project_path, x.source, x.project_name)):
                lines.append(f"### {d.project_name}")
                lines.append(f"- Path: `{d.project_path}`")
                lines.append(f"- Source: `{d.source}`")
                lines.append("")
                lines.append("#### devDependencies")
                lines.append(_to_pretty_json_block(d.dev_dependencies))
                lines.append("")
                lines.append("#### dependencies")
                lines.append(_to_pretty_json_block(d.dependencies))
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"


def _to_pretty_json_block(d: Dict[str, str]) -> str:
    """將 dict 依賴清單輸出成 Markdown code block。"""
    if not d:
        return "_None_"
    items = {k: d[k] for k in sorted(d.keys(), key=str.lower)}
    return "```json\n" + json.dumps(items, ensure_ascii=False, indent=4) + "\n```"


def _select_dependency_manifests(manifests: Sequence[Path]) -> List[Path]:
    """
    將同一個資料夾內「多個依賴描述檔」去重，只保留一份最具代表性的來源。

    背景：
    - 專案常同時存在 `pyproject.toml` 與 `requirements.txt`（歷史遺留或兼容不同工具）。
    - Snapshot 若把同目錄的多份 manifest 全部列出，會讓依賴清單看起來重複。

    目前策略（最小驚喜）：
    - 同目錄優先順序：pyproject.toml > Pipfile > requirements.txt > requirements*.txt（其他）
    - 同一類型多檔案（例如 requirements-dev.txt / requirements-test.txt）僅取排序最前者。
    """

    def sort_key(p: Path) -> Tuple[int, str]:
        if p.name == "pyproject.toml":
            return (0, p.name.lower())
        if p.name == "Pipfile":
            return (1, p.name.lower())
        if p.name == "requirements.txt":
            return (2, p.name.lower())
        if fnmatch.fnmatchcase(p.name, "requirements*.txt"):
            return (3, p.name.lower())
        return (99, p.name.lower())

    by_parent: Dict[Path, List[Path]] = {}
    for m in manifests:
        by_parent.setdefault(m.parent, []).append(m)

    selected: List[Path] = []
    for parent in sorted(by_parent.keys(), key=lambda p: str(p).lower()):
        selected.append(sorted(by_parent[parent], key=sort_key)[0])

    return selected


def _build_arg_parser() -> "argparse.ArgumentParser":
    """建立 snapshot CLI 的 argument parser。"""
    import argparse

    p = argparse.ArgumentParser(description="產出 Python 專案快照（目錄樹 + AST 符號 + 依賴清單）。")
    p.add_argument("root", nargs="?", default=".", help="專案根目錄（預設：目前目錄）")
    p.add_argument("-o", "--output", default="snapshot.md", help="輸出 Markdown 檔案（預設：snapshot.md）")
    p.add_argument("--depth", type=int, default=12, help="目錄樹最大深度（預設：12）")
    p.add_argument("--public-only", action="store_true", help="只輸出 public symbols（忽略 _private / __dunder__）")
    p.add_argument("--include-nested", action="store_true", help="輸出巢狀 symbols（function 內部 def / inner class）")
    p.add_argument("--follow-symlinks", action="store_true", help="跟隨符號連結（預設不啟用）")
    p.add_argument("--no-gitignore", action="store_true", help="不讀取 .gitignore（預設會讀取並套用）")
    p.add_argument("--no-default-excludes", action="store_true", help="不套用預設排除清單（預設會排除 venv/dist/tests 等）")
    p.add_argument("--exclude", action="append", default=[], help="額外排除規則（可重複指定），支援 glob：--exclude \"*.log\"")
    p.add_argument("--max-file-kb", type=int, default=1000, help="單一 Python 檔案最大解析大小（KB，預設：1000）")
    return p


def main(argv: Sequence[str]) -> int:
    """CLI entrypoint：產生 `snapshot.md` 並寫入檔案。"""
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv[1:]))

    root = Path(args.root).resolve()
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output

    config = Config(
        root=root,
        output=output,
        max_tree_depth=max(1, int(args.depth)),
        include_private_symbols=not bool(args.public_only),
        include_nested_symbols=bool(args.include_nested),
        follow_symlinks=bool(args.follow_symlinks),
        use_gitignore=not bool(args.no_gitignore),
        use_default_excludes=not bool(args.no_default_excludes),
        extra_excludes=tuple(args.exclude or []),
        max_file_bytes=max(1, int(args.max_file_kb) * 1024),
    )

    scanner = ProjectScanner(config)
    tree = scanner.build_tree()

    py_parser = PythonFileParser(config)
    file_snaps: List[FileSnapshot] = []
    for p in scanner.iter_python_files():
        fs = py_parser.parse(p)
        if fs.symbols:
            file_snaps.append(fs)

    dep_parser = DependencyParser()
    deps: List[ProjectDeps] = []
    manifests = sorted(
        scanner.iter_dependency_manifests(),
        key=lambda p: (str(p.parent).lower(), p.name.lower()),
    )
    for manifest in _select_dependency_manifests(manifests):
        d = dep_parser.parse_manifest(manifest, root=config.root)
        if d is not None:
            deps.append(d)

    md = ReportGenerator().to_markdown(config=config, tree=tree, file_snaps=file_snaps, deps=deps)
    config.output.write_text(md, encoding="utf-8")
    print(f"[OK] 已輸出 `{config.output}`（{len(md)} 字元）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
