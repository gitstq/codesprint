"""
CodeSprint - Lightweight Multi-Language Code Snippet Intelligent Runner CLI.

A zero-dependency, cross-platform tool for running code snippets in multiple
programming languages with automatic language detection, sandbox execution,
and beautiful TUI output.
"""

__version__ = "1.0.0"
__author__ = "SOLO Agent"
__license__ = "MIT"

from codesprint.runner import CodeRunner
from codesprint.detector import LanguageDetector
from codesprint.executor import Executor
from codesprint.history import HistoryManager
from codesprint.formatter import OutputFormatter

__all__ = [
    "CodeRunner",
    "LanguageDetector",
    "Executor",
    "HistoryManager",
    "OutputFormatter",
    "__version__",
]
