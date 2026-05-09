"""
Code executor module for CodeSprint.

Handles the actual execution of code snippets in a safe,
isolated environment with timeout protection.
"""

import os
import re
import sys
import tempfile
import subprocess
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    output: str
    error: str
    exit_code: int
    execution_time: float
    language: str
    timeout: bool = False

    @property
    def combined_output(self) -> str:
        """Get combined stdout and stderr."""
        if self.output and self.error:
            return f"{self.output}\n{self.error}"
        return self.output or self.error


class Executor:
    """Executes code snippets in multiple languages."""

    # Runtime configurations for each language
    RUNTIMES: Dict[str, Dict] = {
        "python": {
            "command": ["python3", "-c"],
            "file_mode": ["python3"],
            "extension": ".py",
            "check": ["python3", "--version"],
        },
        "javascript": {
            "command": ["node", "-e"],
            "file_mode": ["node"],
            "extension": ".js",
            "check": ["node", "--version"],
        },
        "typescript": {
            "command": ["ts-node", "-e"],
            "file_mode": ["ts-node"],
            "extension": ".ts",
            "check": ["ts-node", "--version"],
            "fallback": ["npx", "ts-node"],
        },
        "go": {
            "command": None,  # Go requires file mode
            "file_mode": ["go", "run"],
            "extension": ".go",
            "check": ["go", "version"],
        },
        "rust": {
            "command": None,  # Rust requires file mode
            "file_mode": ["rustc", "--edition", "2021", "-o"],
            "extension": ".rs",
            "check": ["rustc", "--version"],
            "compile": True,
        },
        "java": {
            "command": None,  # Java requires file mode
            "file_mode": ["java"],
            "extension": ".java",
            "check": ["java", "--version"],
            "compile": True,
            "compile_cmd": ["javac"],
        },
        "c": {
            "command": None,  # C requires file mode
            "file_mode": ["gcc", "-o"],
            "extension": ".c",
            "check": ["gcc", "--version"],
            "compile": True,
        },
        "cpp": {
            "command": None,  # C++ requires file mode
            "file_mode": ["g++", "-o"],
            "extension": ".cpp",
            "check": ["g++", "--version"],
            "compile": True,
        },
        "ruby": {
            "command": ["ruby", "-e"],
            "file_mode": ["ruby"],
            "extension": ".rb",
            "check": ["ruby", "--version"],
        },
        "php": {
            "command": ["php", "-r"],
            "file_mode": ["php"],
            "extension": ".php",
            "check": ["php", "--version"],
        },
        "bash": {
            "command": ["bash", "-c"],
            "file_mode": ["bash"],
            "extension": ".sh",
            "check": ["bash", "--version"],
        },
        "perl": {
            "command": ["perl", "-e"],
            "file_mode": ["perl"],
            "extension": ".pl",
            "check": ["perl", "--version"],
        },
        "lua": {
            "command": ["lua", "-e"],
            "file_mode": ["lua"],
            "extension": ".lua",
            "check": ["lua", "-v"],
        },
        "r": {
            "command": ["Rscript", "-e"],
            "file_mode": ["Rscript"],
            "extension": ".R",
            "check": ["Rscript", "--version"],
        },
        "kotlin": {
            "command": None,
            "file_mode": ["kotlin"],
            "extension": ".kt",
            "check": ["kotlin", "-version"],
            "fallback": ["kotlinc", "-script"],
        },
        "swift": {
            "command": ["swift", "-e"],
            "file_mode": ["swift"],
            "extension": ".swift",
            "check": ["swift", "--version"],
        },
        "scala": {
            "command": ["scala", "-e"],
            "file_mode": ["scala"],
            "extension": ".scala",
            "check": ["scala", "-version"],
        },
    }

    def __init__(
        self,
        timeout: float = 30.0,
        max_output_size: int = 100000,
        work_dir: Optional[str] = None,
    ) -> None:
        """
        Initialize the executor.
        
        Args:
            timeout: Maximum execution time in seconds
            max_output_size: Maximum output size in bytes
            work_dir: Working directory for execution
        """
        self.timeout = timeout
        self.max_output_size = max_output_size
        self.work_dir = work_dir or tempfile.gettempdir()
        self._available_runtimes: Dict[str, bool] = {}
        self._check_runtimes()

    def _check_runtimes(self) -> None:
        """Check which runtimes are available on the system."""
        for lang, config in self.RUNTIMES.items():
            check_cmd = config.get("check", [])
            if check_cmd:
                try:
                    result = subprocess.run(
                        check_cmd,
                        capture_output=True,
                        timeout=5,
                    )
                    self._available_runtimes[lang] = result.returncode == 0
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    self._available_runtimes[lang] = False
            else:
                self._available_runtimes[lang] = False

    def is_available(self, language: str) -> bool:
        """Check if a language runtime is available."""
        return self._available_runtimes.get(language, False)

    def list_available(self) -> List[str]:
        """List all available language runtimes."""
        return [lang for lang, avail in self._available_runtimes.items() if avail]

    def _truncate_output(self, output: str) -> str:
        """Truncate output if it exceeds max size."""
        if len(output) > self.max_output_size:
            return (
                output[: self.max_output_size // 2]
                + "\n\n... [output truncated] ...\n\n"
                + output[-self.max_output_size // 2 :]
            )
        return output

    def _get_java_class_name(self, code: str) -> str:
        """Extract public class name from Java code."""
        match = re.search(r"public\s+class\s+(\w+)", code)
        if match:
            return match.group(1)
        return "Main"

    def execute(
        self,
        code: str,
        language: str,
        filename: Optional[str] = None,
        stdin: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        """
        Execute code snippet.
        
        Args:
            code: Code to execute
            language: Programming language
            filename: Optional filename for context
            stdin: Optional stdin input
            env: Optional environment variables
            
        Returns:
            ExecutionResult with output and status
        """
        config = self.RUNTIMES.get(language)
        if not config:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Unsupported language: {language}",
                exit_code=1,
                execution_time=0.0,
                language=language,
            )

        if not self.is_available(language):
            # Try fallback
            fallback = config.get("fallback")
            if fallback:
                try:
                    subprocess.run(fallback, capture_output=True, timeout=5)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                else:
                    self._available_runtimes[language] = True
            else:
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"Runtime not available for: {language}. "
                    f"Please install the {language} runtime.",
                    exit_code=1,
                    execution_time=0.0,
                    language=language,
                )

        start_time = time.time()
        
        try:
            # Try inline execution first
            if config.get("command"):
                result = self._execute_inline(code, config, stdin, env)
            else:
                result = self._execute_file(code, config, language, filename, stdin, env)
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=self._truncate_output(result.stdout.decode("utf-8", errors="replace")),
                error=self._truncate_output(result.stderr.decode("utf-8", errors="replace")),
                exit_code=result.returncode,
                execution_time=execution_time,
                language=language,
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution timed out after {self.timeout} seconds",
                exit_code=-1,
                execution_time=execution_time,
                language=language,
                timeout=True,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                exit_code=1,
                execution_time=execution_time,
                language=language,
            )

    def _execute_inline(
        self,
        code: str,
        config: Dict,
        stdin: Optional[str],
        env: Optional[Dict[str, str]],
    ) -> subprocess.CompletedProcess:
        """Execute code inline using -e flag."""
        cmd = config["command"] + [code]
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        
        return subprocess.run(
            cmd,
            capture_output=True,
            timeout=self.timeout,
            input=stdin.encode() if stdin else None,
            env=run_env,
            cwd=self.work_dir,
        )

    def _execute_file(
        self,
        code: str,
        config: Dict,
        language: str,
        filename: Optional[str],
        stdin: Optional[str],
        env: Optional[Dict[str, str]],
    ) -> subprocess.CompletedProcess:
        """Execute code from a temporary file."""
        extension = config["extension"]
        
        # Create temp directory for execution
        with tempfile.TemporaryDirectory(dir=self.work_dir) as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Handle special cases
            if language == "java":
                class_name = self._get_java_class_name(code)
                source_file = tmpdir_path / f"{class_name}{extension}"
            else:
                base_name = filename or "code"
                source_file = tmpdir_path / f"{base_name}{extension}"
            
            # Write source code
            source_file.write_text(code, encoding="utf-8")
            
            run_env = os.environ.copy()
            if env:
                run_env.update(env)
            
            # Handle compiled languages
            if config.get("compile"):
                return self._execute_compiled(
                    source_file, tmpdir_path, config, language, stdin, run_env
                )
            
            # Interpret languages
            cmd = config["file_mode"] + [str(source_file)]
            return subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
                input=stdin.encode() if stdin else None,
                env=run_env,
                cwd=str(tmpdir_path),
            )

    def _execute_compiled(
        self,
        source_file: Path,
        tmpdir: Path,
        config: Dict,
        language: str,
        stdin: Optional[str],
        env: Dict[str, str],
    ) -> subprocess.CompletedProcess:
        """Execute compiled language code."""
        output_name = source_file.stem
        
        if language == "java":
            # Compile Java
            compile_cmd = ["javac", str(source_file)]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                timeout=self.timeout,
                cwd=str(tmpdir),
            )
            if compile_result.returncode != 0:
                return compile_result
            
            # Run Java
            run_cmd = ["java", output_name]
            return subprocess.run(
                run_cmd,
                capture_output=True,
                timeout=self.timeout,
                input=stdin.encode() if stdin else None,
                env=env,
                cwd=str(tmpdir),
            )
        
        elif language in ("c", "cpp"):
            # Compile C/C++
            output_file = tmpdir / output_name
            compile_cmd = config["file_mode"] + [str(output_file), str(source_file)]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                timeout=self.timeout,
                cwd=str(tmpdir),
            )
            if compile_result.returncode != 0:
                return compile_result
            
            # Run compiled binary
            return subprocess.run(
                [str(output_file)],
                capture_output=True,
                timeout=self.timeout,
                input=stdin.encode() if stdin else None,
                env=env,
                cwd=str(tmpdir),
            )
        
        elif language == "rust":
            # Compile Rust
            output_file = tmpdir / output_name
            compile_cmd = ["rustc", "--edition", "2021", "-o", str(output_file), str(source_file)]
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                timeout=self.timeout,
                cwd=str(tmpdir),
            )
            if compile_result.returncode != 0:
                return compile_result
            
            # Run compiled binary
            return subprocess.run(
                [str(output_file)],
                capture_output=True,
                timeout=self.timeout,
                input=stdin.encode() if stdin else None,
                env=env,
                cwd=str(tmpdir),
            )
        
        else:
            # Fallback to interpretation
            cmd = config["file_mode"] + [str(source_file)]
            return subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
                input=stdin.encode() if stdin else None,
                env=env,
                cwd=str(tmpdir),
            )
