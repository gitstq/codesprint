"""
Main code runner module for CodeSprint.

Provides the high-level API for running code snippets.
"""

from typing import Optional, Dict, Any
from pathlib import Path

from codesprint.detector import LanguageDetector
from codesprint.executor import Executor, ExecutionResult
from codesprint.history import HistoryManager
from codesprint.formatter import OutputFormatter


class CodeRunner:
    """High-level code runner with history and formatting."""

    def __init__(
        self,
        timeout: float = 30.0,
        history_dir: Optional[str] = None,
        use_color: Optional[bool] = None,
    ) -> None:
        """
        Initialize code runner.
        
        Args:
            timeout: Default execution timeout
            history_dir: Directory for history storage
            use_color: Force color output on/off
        """
        self.detector = LanguageDetector()
        self.executor = Executor(timeout=timeout)
        self.history = HistoryManager(history_dir)
        self.formatter = OutputFormatter(use_color)

    def run(
        self,
        code: str,
        language: Optional[str] = None,
        filename: Optional[str] = None,
        stdin: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        save_history: bool = True,
    ) -> ExecutionResult:
        """
        Run code snippet.
        
        Args:
            code: Code to execute
            language: Programming language (auto-detect if None)
            filename: Optional filename for context
            stdin: Optional stdin input
            env: Optional environment variables
            timeout: Optional timeout override
            save_history: Whether to save to history
            
        Returns:
            ExecutionResult with output and status
        """
        # Detect language if not specified
        if language is None:
            language, confidence = self.detector.detect(code, filename)
            if language == "text" and confidence == 0.0:
                # Could not detect, default to python
                language = "python"
        
        # Override timeout if specified
        if timeout is not None:
            original_timeout = self.executor.timeout
            self.executor.timeout = timeout
        
        try:
            # Execute code
            result = self.executor.execute(
                code=code,
                language=language,
                filename=filename,
                stdin=stdin,
                env=env,
            )
            
            # Save to history
            if save_history:
                self.history.add_entry(
                    code=code,
                    language=language,
                    output=result.output,
                    error=result.error,
                    success=result.success,
                    execution_time=result.execution_time,
                    filename=filename,
                )
            
            return result
            
        finally:
            if timeout is not None:
                self.executor.timeout = original_timeout

    def run_file(
        self,
        filepath: str,
        language: Optional[str] = None,
        stdin: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ExecutionResult:
        """
        Run code from file.
        
        Args:
            filepath: Path to source file
            language: Programming language (auto-detect if None)
            stdin: Optional stdin input
            env: Optional environment variables
            timeout: Optional timeout override
            
        Returns:
            ExecutionResult with output and status
        """
        path = Path(filepath)
        
        if not path.exists():
            return ExecutionResult(
                success=False,
                output="",
                error=f"File not found: {filepath}",
                exit_code=1,
                execution_time=0.0,
                language=language or "unknown",
            )
        
        code = path.read_text(encoding="utf-8")
        filename = path.name
        
        # Detect from extension if language not specified
        if language is None:
            language = self.detector.detect_from_extension(filename)
        
        return self.run(
            code=code,
            language=language,
            filename=filename,
            stdin=stdin,
            env=env,
            timeout=timeout,
        )

    def format_result(self, result: ExecutionResult) -> str:
        """Format execution result for display."""
        return self.formatter.format_result(
            output=result.output,
            error=result.error,
            success=result.success,
            execution_time=result.execution_time,
            language=result.language,
        )

    def get_available_languages(self) -> list:
        """Get list of available language runtimes."""
        return self.executor.list_available()

    def get_supported_languages(self) -> list:
        """Get list of all supported languages."""
        return self.detector.list_languages()

    def get_history(self, limit: int = 20) -> list:
        """Get recent history entries."""
        history = self.history.load_history()
        return history[:limit]

    def get_stats(self) -> Dict[str, Any]:
        """Get history statistics."""
        return self.history.get_stats()

    def clear_history(self) -> None:
        """Clear all history."""
        self.history.clear_history()

    def search_history(
        self,
        query: str,
        language: Optional[str] = None,
    ) -> list:
        """Search history entries."""
        return self.history.search(query, language)
