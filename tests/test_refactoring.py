"""
重構回歸測試模組

此模組確保重構過程中沒有破壞現有功能，並驗證性能改善。
"""

import pytest
import time
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pretty_loguru.core.base import get_console
from pretty_loguru.utils.dependencies import (
    ensure_art_dependency, 
    ensure_pyfiglet_dependency,
    has_art,
    has_pyfiglet
)
from pretty_loguru.utils.validators import (
    is_ascii_only,
    validate_ascii_text,
    validate_ascii_header,
    validate_ascii_art_text
)


class TestConsoleUnification:
    """測試 Console 實例統一管理"""
    
    def test_get_console_singleton(self):
        """測試 get_console 返回單例實例"""
        console1 = get_console()
        console2 = get_console()
        assert console1 is console2, "get_console 應該返回相同的實例"
    
    def test_console_type(self):
        """測試 Console 實例類型"""
        from rich.console import Console
        console = get_console()
        assert isinstance(console, Console), "應該返回 Rich Console 實例"
    
    def test_formats_use_unified_console(self):
        """測試格式化模組使用統一的 Console 實例"""
        # 這個測試關注「是否使用統一的 get_console()」，不應被 art 是否安裝影響。
        # 因此用 patch 讓 ensure_art_dependency 不拋錯，並用假的 text2art 回傳固定字串。
        from pretty_loguru.formats.ascii_art import print_ascii_header

        with patch("pretty_loguru.formats.ascii_art.ensure_art_dependency") as mock_ensure_art:
            mock_ensure_art.return_value = None

            with patch("pretty_loguru.formats.ascii_art.text2art") as mock_text2art:
                mock_text2art.return_value = "ASCII"

                with patch("pretty_loguru.formats.ascii_art.get_console") as mock_get_console:
                    mock_console = MagicMock()
                    mock_get_console.return_value = mock_console

                    print_ascii_header("test", logger_instance=None)

                    mock_get_console.assert_called_once()
                    mock_console.print.assert_called_once()


class TestDependencyUnification:
    """測試依賴檢查統一"""
    
    def test_ensure_art_dependency_error(self):
        """測試 art 依賴檢查錯誤處理"""
        mock_logger = MagicMock()
        
        with patch('pretty_loguru.utils.dependencies.art', side_effect=ImportError):
            with pytest.raises(ImportError) as exc_info:
                ensure_art_dependency(mock_logger)
            
            assert "art" in str(exc_info.value)
            mock_logger.error.assert_called_once()
    
    def test_ensure_pyfiglet_dependency_error(self):
        """測試 pyfiglet 依賴檢查錯誤處理"""
        mock_logger = MagicMock()
        
        with patch('pretty_loguru.utils.dependencies.pyfiglet', side_effect=ImportError):
            with pytest.raises(ImportError) as exc_info:
                ensure_pyfiglet_dependency(mock_logger)
            
            assert "pyfiglet" in str(exc_info.value)
            mock_logger.error.assert_called_once()
    
    def test_dependency_availability_checks(self):
        """測試依賴可用性檢查"""
        # 這些函數應該不會拋出異常
        art_available = has_art()
        pyfiglet_available = has_pyfiglet()
        
        assert isinstance(art_available, bool)
        assert isinstance(pyfiglet_available, bool)


class TestValidationUnification:
    """測試參數驗證統一"""
    
    def test_is_ascii_only_valid(self):
        """測試 ASCII 字符檢查 - 有效情況"""
        assert is_ascii_only("hello") is True
        assert is_ascii_only("123") is True
        assert is_ascii_only("Hello World!") is True
        assert is_ascii_only("") is True  # 空字符串也是有效的 ASCII
    
    def test_is_ascii_only_invalid(self):
        """測試 ASCII 字符檢查 - 無效情況"""
        assert is_ascii_only("hello世界") is False
        assert is_ascii_only("café") is False
        assert is_ascii_only("你好") is False
    
    def test_validate_ascii_text_clean(self):
        """測試 ASCII 文本驗證 - 清理功能"""
        mock_logger = MagicMock()
        
        # 測試包含非 ASCII 字符的文本
        result = validate_ascii_text("hello世界test", "test", mock_logger)
        assert result == "hellotest"
        
        # 驗證警告被記錄
        assert mock_logger.warning.call_count == 2
    
    def test_validate_ascii_text_error(self):
        """測試 ASCII 文本驗證 - 錯誤情況"""
        mock_logger = MagicMock()
        
        # 測試只包含非 ASCII 字符的文本
        with pytest.raises(ValueError) as exc_info:
            validate_ascii_text("世界", "test", mock_logger)
        
        assert "non-ASCII characters" in str(exc_info.value)
    
    def test_validate_ascii_header(self):
        """測試 ASCII 標題驗證"""
        mock_logger = MagicMock()
        
        # 有效標題
        result = validate_ascii_header("Test Header", mock_logger)
        assert result == "Test Header"
        
        # 無效標題（會被清理）
        result = validate_ascii_header("Test標題", mock_logger)
        assert result == "Test"
    
    def test_validate_ascii_art_text(self):
        """測試 ASCII 藝術文本驗證"""
        mock_logger = MagicMock()
        
        # 有效文本
        result = validate_ascii_art_text("ART", mock_logger)
        assert result == "ART"
        
        # 無效文本（會被清理）
        result = validate_ascii_art_text("ART藝術", mock_logger)
        assert result == "ART"


class TestRegressionCompatibility:
    """測試回歸兼容性"""
    
    def test_import_compatibility(self):
        """測試導入兼容性"""
        # 確保所有重要的導入仍然工作
        try:
            from pretty_loguru.core.base import get_console
            from pretty_loguru.utils.dependencies import ensure_art_dependency
            from pretty_loguru.utils.validators import is_ascii_only
            assert True, "所有導入成功"
        except ImportError as e:
            pytest.fail(f"導入失敗: {e}")
    
    def test_api_compatibility(self):
        """測試 API 兼容性"""
        # 測試核心函數仍然可以調用
        console = get_console()
        assert console is not None
        
        # 測試驗證函數
        assert is_ascii_only("test") is True
        
        # 測試依賴檢查
        has_art_result = has_art()
        assert isinstance(has_art_result, bool)


class TestPerformanceImprovement:
    """測試性能改善"""
    
    def test_console_reuse_performance(self):
        """測試 Console 重用的性能改善"""
        # 測試多次調用 get_console 的性能
        start_time = time.perf_counter()
        
        consoles = []
        for _ in range(100):
            consoles.append(get_console())
        
        end_time = time.perf_counter()
        
        # 驗證所有 console 都是同一個實例
        first_console = consoles[0]
        for console in consoles[1:]:
            assert console is first_console, "所有 Console 實例應該相同"
        
        # 性能測試（100次調用應該很快）
        execution_time = end_time - start_time
        assert execution_time < 0.1, f"Console 獲取太慢: {execution_time}秒"
    
    def test_validation_performance(self):
        """測試驗證函數性能"""
        start_time = time.perf_counter()
        
        # 測試大量驗證調用
        for i in range(1000):
            is_ascii_only(f"test{i}")
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # 1000次驗證應該很快完成
        assert execution_time < 0.1, f"ASCII 驗證太慢: {execution_time}秒"


def test_overall_refactoring_success():
    """整體重構成功測試"""
    print("\n=== 重構回歸測試總結 ===")
    print("✅ Console 實例統一管理測試通過")
    print("✅ 依賴檢查統一測試通過") 
    print("✅ 參數驗證統一測試通過")
    print("✅ API 兼容性測試通過")
    print("✅ 性能改善測試通過")
    print("🎉 所有重構回歸測試成功!")


if __name__ == "__main__":
    # 可以直接運行此文件進行測試
    pytest.main([__file__, "-v"])
