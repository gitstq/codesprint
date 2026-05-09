"""
Output formatting module for CodeSprint.

Provides beautiful, colorful terminal output with syntax highlighting
and various export formats.
"""

import sys
import re
from typing import Optional, Dict, List, Any
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    
    # Reset
    RESET = "\033[0m"
    
    # Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    
    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports colors."""
        # Check if stdout is a terminal
        if not hasattr(sys.stdout, "isatty"):
            return False
        if not sys.stdout.isatty():
            return False
        
        # Check for NO_COLOR environment variable
        if os.environ.get("NO_COLOR"):
            return False
        
        # Check for Windows
        if sys.platform == "win32":
            # Windows Terminal and modern cmd support colors
            return True
        
        return True


import os


class OutputFormatter:
    """Formats output for terminal display."""

    # Language-specific syntax highlighting patterns
    SYNTAX_PATTERNS: Dict[str, List[tuple]] = {
        "python": [
            (r"\b(import|from|as|def|class|if|elif|else|for|while|try|except|finally|with|return|yield|raise|break|continue|pass|lambda|and|or|not|in|is|None|True|False)\b", "keyword"),
            (r"\b(int|float|str|list|dict|set|tuple|bool|bytes|object)\b", "type"),
            (r"#.*$", "comment"),
            (r'""".*?"""', "string"),
            (r"'''.*?'''", "string"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"'[^'\\]*(?:\\.[^'\\]*)*'", "string"),
            (r"\b(\d+\.?\d*)\b", "number"),
            (r"\b([A-Z][a-zA-Z0-9_]*)\b", "class"),
        ],
        "javascript": [
            (r"\b(const|let|var|function|class|if|else|for|while|do|switch|case|break|continue|return|yield|async|await|try|catch|finally|throw|new|this|super|extends|import|export|from|as|default)\b", "keyword"),
            (r"\b(true|false|null|undefined|NaN|Infinity)\b", "constant"),
            (r"//.*$", "comment"),
            (r"/\*[\s\S]*?\*/", "comment"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"'[^'\\]*(?:\\.[^'\\]*)*'", "string"),
            (r"`[^`\\]*(?:\\.[^`\\]*)*`", "string"),
            (r"\b(\d+\.?\d*)\b", "number"),
        ],
        "go": [
            (r"\b(package|import|func|var|const|type|struct|interface|if|else|for|range|switch|case|default|break|continue|return|go|defer|chan|select)\b", "keyword"),
            (r"\b(true|false|nil)\b", "constant"),
            (r"//.*$", "comment"),
            (r"/\*[\s\S]*?\*/", "comment"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"`[^`]*`", "string"),
            (r"\b(\d+\.?\d*)\b", "number"),
        ],
        "rust": [
            (r"\b(fn|let|mut|const|static|pub|mod|use|struct|enum|impl|trait|type|if|else|match|for|while|loop|break|continue|return|async|await|move|ref|self|Self|where|unsafe)\b", "keyword"),
            (r"\b(true|false|Some|None|Ok|Err)\b", "constant"),
            (r"//.*$", "comment"),
            (r"/\*[\s\S]*?\*/", "comment"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"\b(\d+\.?\d*)\b", "number"),
        ],
        "java": [
            (r"\b(package|import|public|private|protected|class|interface|extends|implements|new|this|super|static|final|abstract|synchronized|volatile|transient|native|strictfp|if|else|for|while|do|switch|case|default|break|continue|return|throw|throws|try|catch|finally|void|int|long|short|byte|float|double|boolean|char)\b", "keyword"),
            (r"\b(true|false|null)\b", "constant"),
            (r"//.*$", "comment"),
            (r"/\*[\s\S]*?\*/", "comment"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"\b(\d+\.?\d*[fFdDlL]?)\b", "number"),
        ],
        "bash": [
            (r"\b(if|then|else|elif|fi|for|while|do|done|case|esac|function|return|exit|break|continue|local|export|readonly|declare|unset|shift|source|eval|exec)\b", "keyword"),
            (r"#.*$", "comment"),
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', "string"),
            (r"'[^']*'", "string"),
            (r"\$\{?\w+\}?", "variable"),
        ],
    }

    def __init__(self, use_color: Optional[bool] = None) -> None:
        """
        Initialize formatter.
        
        Args:
            use_color: Force color on/off, None for auto-detect
        """
        if use_color is None:
            self.use_color = Colors.supports_color()
        else:
            self.use_color = use_color
        
        # Color scheme for syntax highlighting
        self.color_map = {
            "keyword": Colors.CYAN + Colors.BOLD,
            "type": Colors.YELLOW,
            "constant": Colors.MAGENTA,
            "string": Colors.GREEN,
            "number": Colors.BRIGHT_YELLOW,
            "comment": Colors.DIM + Colors.BRIGHT_BLACK,
            "class": Colors.BRIGHT_BLUE,
            "variable": Colors.BRIGHT_CYAN,
        }

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text."""
        if not self.use_color:
            return text
        return f"{color}{text}{Colors.RESET}"

    def format_header(self, text: str, char: str = "═") -> str:
        """Format a header with decoration."""
        if not self.use_color:
            return f"\n{text}\n{'─' * len(text)}"
        
        width = max(len(text) + 4, 60)
        return (
            f"\n{Colors.BRIGHT_CYAN}{char * width}{Colors.RESET}\n"
            f"{Colors.BOLD}{Colors.BRIGHT_WHITE}  {text}  {Colors.RESET}\n"
            f"{Colors.BRIGHT_CYAN}{char * width}{Colors.RESET}\n"
        )

    def format_section(self, title: str, content: str) -> str:
        """Format a section with title and content."""
        if not self.use_color:
            return f"\n[{title}]\n{content}"
        
        return (
            f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}▶ {title}{Colors.RESET}\n"
            f"{Colors.DIM}{'─' * 40}{Colors.RESET}\n"
            f"{content}\n"
        )

    def format_code(
        self,
        code: str,
        language: Optional[str] = None,
        line_numbers: bool = True,
    ) -> str:
        """
        Format code with syntax highlighting.
        
        Args:
            code: Source code to format
            language: Programming language for highlighting
            line_numbers: Show line numbers
        """
        lines = code.split("\n")
        formatted_lines = []
        
        # Get patterns for language
        patterns = self.SYNTAX_PATTERNS.get(language, []) if language else []
        
        for i, line in enumerate(lines, 1):
            # Apply syntax highlighting
            highlighted = line
            for pattern, token_type in patterns:
                color = self.color_map.get(token_type, "")
                if color:
                    highlighted = re.sub(
                        pattern,
                        lambda m: self._colorize(m.group(0), color),
                        highlighted,
                        flags=re.MULTILINE,
                    )
            
            # Add line number
            if line_numbers:
                line_num = self._colorize(f"{i:4d} │ ", Colors.DIM + Colors.BRIGHT_BLACK)
                formatted_lines.append(f"{line_num}{highlighted}")
            else:
                formatted_lines.append(highlighted)
        
        return "\n".join(formatted_lines)

    def format_output(
        self,
        output: str,
        success: bool = True,
        max_lines: int = 100,
    ) -> str:
        """Format execution output."""
        lines = output.strip().split("\n")
        
        # Truncate if too many lines
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append(self._colorize("... [output truncated]", Colors.DIM))
        
        # Color based on success
        if success:
            prefix = self._colorize("  ", Colors.BG_GREEN)
        else:
            prefix = self._colorize("  ", Colors.BG_RED)
        
        formatted = []
        for line in lines:
            formatted.append(f"{prefix} {line}")
        
        return "\n".join(formatted)

    def format_error(self, error: str) -> str:
        """Format error message."""
        if not self.use_color:
            return f"\n❌ Error:\n{error}"
        
        return (
            f"\n{Colors.BG_RED}{Colors.BRIGHT_WHITE} ❌ Error {Colors.RESET}\n"
            f"{Colors.RED}{error}{Colors.RESET}\n"
        )

    def format_result(
        self,
        output: str,
        error: str,
        success: bool,
        execution_time: float,
        language: str,
    ) -> str:
        """Format complete execution result."""
        lines = []
        
        # Status header
        if success:
            status = self._colorize("✅ SUCCESS", Colors.BRIGHT_GREEN + Colors.BOLD)
        else:
            status = self._colorize("❌ FAILED", Colors.BRIGHT_RED + Colors.BOLD)
        
        time_str = self._colorize(f"{execution_time:.3f}s", Colors.BRIGHT_YELLOW)
        lang_str = self._colorize(language.upper(), Colors.BRIGHT_CYAN)
        
        lines.append(f"\n{status}  {lang_str}  ⏱ {time_str}")
        lines.append(self._colorize("─" * 50, Colors.DIM))
        
        # Output
        if output:
            lines.append(self._colorize("\n📤 Output:", Colors.BRIGHT_BLUE))
            lines.append(self.format_output(output, success))
        
        # Error
        if error:
            lines.append(self.format_error(error))
        
        return "\n".join(lines)

    def format_history_entry(
        self,
        entry_id: str,
        language: str,
        success: bool,
        timestamp: str,
        preview: str = "",
    ) -> str:
        """Format a history entry for display."""
        # Status icon
        icon = "✅" if success else "❌"
        status_color = Colors.BRIGHT_GREEN if success else Colors.BRIGHT_RED
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            time_str = timestamp
        
        if not self.use_color:
            return f"{icon} [{entry_id}] {language} - {time_str}\n  {preview[:60]}..."
        
        return (
            f"{self._colorize(icon, status_color)} "
            f"{self._colorize(entry_id, Colors.DIM)} "
            f"{self._colorize(language, Colors.BRIGHT_CYAN)} "
            f"- {time_str}\n"
            f"  {self._colorize(preview[:60], Colors.DIM)}..."
        )

    def format_stats(self, stats: Dict[str, Any]) -> str:
        """Format history statistics."""
        lines = [self.format_header("📊 History Statistics")]
        
        # Basic stats
        avg_time = f"{stats['avg_execution_time']:.3f}s"
        lines.append(
            f"  Total executions: {self._colorize(str(stats['total']), Colors.BRIGHT_WHITE)}\n"
            f"  Successful: {self._colorize(str(stats['successful']), Colors.BRIGHT_GREEN)}\n"
            f"  Failed: {self._colorize(str(stats['failed']), Colors.BRIGHT_RED)}\n"
            f"  Favorites: {self._colorize(str(stats['favorites']), Colors.BRIGHT_YELLOW)}\n"
            f"  Avg time: {self._colorize(avg_time, Colors.BRIGHT_CYAN)}\n"
        )
        
        # Language breakdown
        if stats["languages"]:
            lines.append(self._colorize("\n  Languages:", Colors.BRIGHT_BLUE))
            for lang, count in sorted(stats["languages"].items(), key=lambda x: -x[1]):
                bar = "█" * min(count // 2, 20)
                lines.append(f"    {lang:12} {self._colorize(bar, Colors.CYAN)} {count}")
        
        return "\n".join(lines)

    def format_available_runtimes(self, runtimes: List[str]) -> str:
        """Format list of available runtimes."""
        lines = [self.format_header("🔧 Available Runtimes")]
        
        if not runtimes:
            lines.append(self._colorize("  No runtimes available", Colors.BRIGHT_RED))
        else:
            for runtime in sorted(runtimes):
                lines.append(f"  {self._colorize('✓', Colors.BRIGHT_GREEN)} {runtime}")
        
        return "\n".join(lines)

    def format_help(self) -> str:
        """Format help message."""
        help_text = """
CodeSprint - Lightweight Multi-Language Code Snippet Runner

Usage:
  codesprint <file>              Run code from file
  codesprint -c <code>           Run code from command line
  codesprint -i                  Interactive REPL mode
  codesprint -l                  List available runtimes
  codesprint -h                  Show this help

Options:
  -c, --code <code>      Code to execute
  -l, --lang <language>  Specify language (auto-detect if not specified)
  -t, --timeout <sec>    Execution timeout (default: 30)
  -H, --history          Show execution history
  -s, --stats            Show history statistics
  -i, --interactive      Interactive REPL mode
  -L, --list             List available runtimes
  -v, --version          Show version
  -h, --help             Show this help

Examples:
  codesprint script.py
  codesprint -c "print('Hello, World!')"
  codesprint -l python -c "import sys; print(sys.version)"
  codesprint -i
  codesprint -H

Supported Languages:
  Python, JavaScript, TypeScript, Go, Rust, Java, C, C++,
  Ruby, PHP, Bash, Perl, Lua, R, Kotlin, Swift, Scala
"""
        if self.use_color:
            # Colorize the help text
            help_text = re.sub(
                r"(codesprint [^\n]+)",
                lambda m: self._colorize(m.group(0), Colors.BRIGHT_CYAN),
                help_text,
            )
            help_text = re.sub(
                r"(-[a-zA-Z], --[a-z-]+)",
                lambda m: self._colorize(m.group(0), Colors.BRIGHT_YELLOW),
                help_text,
            )
        
        return help_text
