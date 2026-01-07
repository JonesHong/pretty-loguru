from __future__ import annotations


def missing_dependency(dep_name: str, *, extra: str | None = None) -> ImportError:
    """
    統一 integrations 的缺依賴錯誤訊息（避免 import-time warning）。

    Args:
        dep_name: 缺少的套件名稱（例如 "fastapi" / "uvicorn"）
        extra: 建議的 extras 名稱（例如 "integrations"）
    """

    install_hint = f'pip install "pretty-loguru[{extra}]"' if extra else f"pip install {dep_name}"
    return ImportError(f"未安裝 {dep_name} 套件，無法使用此整合。請執行：{install_hint}")

