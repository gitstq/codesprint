"""Tests for CodeSprint."""

import pytest
from codesprint.detector import LanguageDetector
from codesprint.executor import Executor, ExecutionResult
from codesprint.history import HistoryManager, HistoryEntry
from codesprint.formatter import OutputFormatter, Colors


class TestLanguageDetector:
    """Tests for LanguageDetector."""
    
    def setup_method(self) -> None:
        self.detector = LanguageDetector()
    
    def test_detect_python_from_extension(self) -> None:
        """Test Python detection from file extension."""
        assert self.detector.detect_from_extension("test.py") == "python"
        assert self.detector.detect_from_extension("script.pyw") == "python"
    
    def test_detect_javascript_from_extension(self) -> None:
        """Test JavaScript detection from file extension."""
        assert self.detector.detect_from_extension("app.js") == "javascript"
        assert self.detector.detect_from_extension("module.mjs") == "javascript"
    
    def test_detect_go_from_extension(self) -> None:
        """Test Go detection from file extension."""
        assert self.detector.detect_from_extension("main.go") == "go"
    
    def test_detect_python_from_shebang(self) -> None:
        """Test Python detection from shebang."""
        code = "#!/usr/bin/env python\nprint('hello')"
        assert self.detector.detect_from_shebang(code) == "python"
    
    def test_detect_bash_from_shebang(self) -> None:
        """Test Bash detection from shebang."""
        code = "#!/bin/bash\necho hello"
        assert self.detector.detect_from_shebang(code) == "bash"
    
    def test_detect_python_from_patterns(self) -> None:
        """Test Python detection from code patterns."""
        code = "import os\nprint('hello')"
        assert self.detector.detect_from_patterns(code) == "python"
    
    def test_detect_javascript_from_patterns(self) -> None:
        """Test JavaScript detection from code patterns."""
        code = "const x = 10;\nconsole.log(x);"
        assert self.detector.detect_from_patterns(code) == "javascript"
    
    def test_detect_with_confidence(self) -> None:
        """Test detection with confidence score."""
        code = "print('hello')"
        lang, confidence = self.detector.detect(code)
        assert lang in ("python", "text")
        assert confidence >= 0.0
    
    def test_list_languages(self) -> None:
        """Test listing supported languages."""
        languages = self.detector.list_languages()
        assert "python" in languages
        assert "javascript" in languages
        assert "go" in languages


class TestExecutor:
    """Tests for Executor."""
    
    def setup_method(self) -> None:
        self.executor = Executor(timeout=5.0)
    
    def test_is_available(self) -> None:
        """Test runtime availability check."""
        # Python should always be available in test environment
        assert self.executor.is_available("python") is True
    
    def test_list_available(self) -> None:
        """Test listing available runtimes."""
        available = self.executor.list_available()
        assert "python" in available
    
    def test_execute_python_code(self) -> None:
        """Test executing Python code."""
        result = self.executor.execute(
            code="print('Hello, World!')",
            language="python",
        )
        assert result.success is True
        assert "Hello, World!" in result.output
        assert result.exit_code == 0
    
    def test_execute_python_with_error(self) -> None:
        """Test executing Python code with error."""
        result = self.executor.execute(
            code="raise ValueError('test error')",
            language="python",
        )
        assert result.success is False
        assert "test error" in result.error
    
    def test_execute_with_timeout(self) -> None:
        """Test execution timeout."""
        executor = Executor(timeout=0.1)
        result = executor.execute(
            code="import time; time.sleep(10)",
            language="python",
        )
        assert result.timeout is True
        assert result.success is False


class TestHistoryManager:
    """Tests for HistoryManager."""
    
    def setup_method(self) -> None:
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.history = HistoryManager(history_dir=self.temp_dir)
    
    def teardown_method(self) -> None:
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_entry(self) -> None:
        """Test adding history entry."""
        entry = self.history.add_entry(
            code="print('test')",
            language="python",
            output="test\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        assert entry.id is not None
        assert entry.language == "python"
        assert entry.success is True
    
    def test_load_history(self) -> None:
        """Test loading history."""
        self.history.add_entry(
            code="print('test1')",
            language="python",
            output="test1\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        self.history.add_entry(
            code="print('test2')",
            language="python",
            output="test2\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        
        entries = self.history.load_history()
        assert len(entries) == 2
    
    def test_get_entry(self) -> None:
        """Test getting specific entry."""
        entry = self.history.add_entry(
            code="print('test')",
            language="python",
            output="test\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        
        retrieved = self.history.get_entry(entry.id)
        assert retrieved is not None
        assert retrieved.code == "print('test')"
    
    def test_toggle_favorite(self) -> None:
        """Test toggling favorite status."""
        entry = self.history.add_entry(
            code="print('test')",
            language="python",
            output="test\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        
        assert entry.favorite is False
        self.history.toggle_favorite(entry.id)
        
        retrieved = self.history.get_entry(entry.id)
        assert retrieved.favorite is True
    
    def test_search(self) -> None:
        """Test searching history."""
        self.history.add_entry(
            code="print('hello world')",
            language="python",
            output="hello world\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        self.history.add_entry(
            code="console.log('test')",
            language="javascript",
            output="test\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        
        results = self.history.search("hello")
        assert len(results) == 1
        assert results[0].language == "python"
    
    def test_get_stats(self) -> None:
        """Test getting statistics."""
        self.history.add_entry(
            code="print('test1')",
            language="python",
            output="test1\n",
            error="",
            success=True,
            execution_time=0.1,
        )
        self.history.add_entry(
            code="raise Error",
            language="python",
            output="",
            error="Error",
            success=False,
            execution_time=0.05,
        )
        
        stats = self.history.get_stats()
        assert stats["total"] == 2
        assert stats["successful"] == 1
        assert stats["failed"] == 1


class TestOutputFormatter:
    """Tests for OutputFormatter."""
    
    def setup_method(self) -> None:
        self.formatter = OutputFormatter(use_color=False)
    
    def test_format_header(self) -> None:
        """Test header formatting."""
        result = self.formatter.format_header("Test Header")
        assert "Test Header" in result
    
    def test_format_code(self) -> None:
        """Test code formatting."""
        code = "print('hello')"
        result = self.formatter.format_code(code, language="python")
        assert "print" in result
    
    def test_format_result(self) -> None:
        """Test result formatting."""
        result = self.formatter.format_result(
            output="hello\n",
            error="",
            success=True,
            execution_time=0.1,
            language="python",
        )
        assert "SUCCESS" in result
        assert "PYTHON" in result
    
    def test_format_error(self) -> None:
        """Test error formatting."""
        result = self.formatter.format_error("Test error")
        assert "Error" in result
        assert "Test error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
