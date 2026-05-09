"""
Language detection module for CodeSprint.

Automatically detects programming language from file extension,
shebang line, or code content patterns.
"""

import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple


class LanguageDetector:
    """Detects programming language from various sources."""

    # Language configurations with extensions, shebangs, and patterns
    LANGUAGES: Dict[str, Dict] = {
        "python": {
            "extensions": [".py", ".pyw", ".py3"],
            "shebangs": ["python", "python3", "python2"],
            "patterns": [
                r"^import\s+\w+",
                r"^from\s+\w+\s+import",
                r"^def\s+\w+\s*\(",
                r"^class\s+\w+.*:",
                r"^if\s+__name__\s*==\s*['\"]__main__['\"]",
                r"^print\s*\(",
                r"^async\s+def\s+\w+",
            ],
            "comment": "#",
        },
        "javascript": {
            "extensions": [".js", ".mjs", ".cjs"],
            "shebangs": ["node", "nodejs", "deno"],
            "patterns": [
                r"^const\s+\w+\s*=",
                r"^let\s+\w+\s*=",
                r"^var\s+\w+\s*=",
                r"^function\s+\w+\s*\(",
                r"^async\s+function",
                r"^=>\s*\{",
                r"console\.log\s*\(",
            ],
            "comment": "//",
        },
        "typescript": {
            "extensions": [".ts", ".tsx", ".mts", ".cts"],
            "shebangs": ["ts-node", "deno"],
            "patterns": [
                r"^interface\s+\w+",
                r"^type\s+\w+\s*=",
                r":\s*(string|number|boolean|any)\b",
                r"^enum\s+\w+",
                r"<\w+>",
            ],
            "comment": "//",
        },
        "go": {
            "extensions": [".go"],
            "shebangs": [],
            "patterns": [
                r"^package\s+\w+",
                r"^func\s+\w+\s*\(",
                r"^func\s+\(\w+\s+\*?\w+\)",
                r"^import\s*\(",
                r"fmt\.Print",
            ],
            "comment": "//",
        },
        "rust": {
            "extensions": [".rs"],
            "shebangs": [],
            "patterns": [
                r"^fn\s+\w+\s*\(",
                r"^let\s+mut\s+\w+",
                r"^use\s+\w+",
                r"^pub\s+fn\s+\w+",
                r"^struct\s+\w+",
                r"^impl\s+\w+",
                r"println!\s*\(",
            ],
            "comment": "//",
        },
        "java": {
            "extensions": [".java"],
            "shebangs": [],
            "patterns": [
                r"^public\s+class\s+\w+",
                r"^package\s+[\w\.]+;",
                r"^import\s+java\.",
                r"^public\s+static\s+void\s+main",
                r"System\.out\.print",
            ],
            "comment": "//",
        },
        "c": {
            "extensions": [".c", ".h"],
            "shebangs": [],
            "patterns": [
                r"^#include\s*<",
                r"^int\s+main\s*\(",
                r"^void\s+\w+\s*\(",
                r"printf\s*\(",
            ],
            "comment": "//",
        },
        "cpp": {
            "extensions": [".cpp", ".cxx", ".cc", ".hpp", ".hxx"],
            "shebangs": [],
            "patterns": [
                r"^#include\s*<",
                r"^using\s+namespace\s+",
                r"std::",
                r"cout\s*<<",
                r"cin\s*>>",
            ],
            "comment": "//",
        },
        "ruby": {
            "extensions": [".rb", ".rbw"],
            "shebangs": ["ruby"],
            "patterns": [
                r"^def\s+\w+",
                r"^class\s+\w+",
                r"^require\s+['\"]",
                r"^puts\s+",
                r"^end\s*$",
            ],
            "comment": "#",
        },
        "php": {
            "extensions": [".php", ".phtml", ".php3", ".php4", ".php5"],
            "shebangs": ["php"],
            "patterns": [
                r"^<\?php",
                r"^\$\w+\s*=",
                r"^function\s+\w+\s*\(",
                r"echo\s+",
            ],
            "comment": "//",
        },
        "bash": {
            "extensions": [".sh", ".bash", ".zsh"],
            "shebangs": ["bash", "sh", "zsh", "dash"],
            "patterns": [
                r"^#!/",
                r"^echo\s+",
                r"^if\s+\[\[",
                r"^for\s+\w+\s+in",
                r"^\$\{?\w+\}?",
            ],
            "comment": "#",
        },
        "perl": {
            "extensions": [".pl", ".pm", ".t"],
            "shebangs": ["perl"],
            "patterns": [
                r"^use\s+strict",
                r"^use\s+warnings",
                r"^sub\s+\w+",
                r"^my\s+\$\w+",
                r"print\s+",
            ],
            "comment": "#",
        },
        "lua": {
            "extensions": [".lua"],
            "shebangs": ["lua"],
            "patterns": [
                r"^function\s+\w+\s*\(",
                r"^local\s+\w+\s*=",
                r"^require\s+['\"]",
                r"print\s*\(",
            ],
            "comment": "--",
        },
        "r": {
            "extensions": [".r", ".R", ".rmd"],
            "shebangs": ["Rscript"],
            "patterns": [
                r"^library\s*\(",
                r"^function\s*\(",
                r"<-\s*function",
                r"print\s*\(",
                r"cat\s*\(",
            ],
            "comment": "#",
        },
        "kotlin": {
            "extensions": [".kt", ".kts"],
            "shebangs": ["kotlin"],
            "patterns": [
                r"^fun\s+\w+\s*\(",
                r"^package\s+[\w\.]+",
                r"^import\s+kotlin\.",
                r"^class\s+\w+",
                r"^object\s+\w+",
            ],
            "comment": "//",
        },
        "swift": {
            "extensions": [".swift"],
            "shebangs": ["swift"],
            "patterns": [
                r"^import\s+\w+",
                r"^func\s+\w+\s*\(",
                r"^var\s+\w+\s*:",
                r"^let\s+\w+\s*=",
                r"print\s*\(",
            ],
            "comment": "//",
        },
        "scala": {
            "extensions": [".scala", ".sc"],
            "shebangs": ["scala"],
            "patterns": [
                r"^object\s+\w+",
                r"^class\s+\w+",
                r"^def\s+\w+\s*\(",
                r"^import\s+scala\.",
                r"println\s*\(",
            ],
            "comment": "//",
        },
    }

    def __init__(self) -> None:
        """Initialize the language detector."""
        self._extension_map: Dict[str, str] = {}
        self._shebang_map: Dict[str, str] = {}
        
        for lang, config in self.LANGUAGES.items():
            for ext in config["extensions"]:
                self._extension_map[ext.lower()] = lang
            for shebang in config["shebangs"]:
                self._shebang_map[shebang] = lang

    def detect_from_extension(self, filename: str) -> Optional[str]:
        """Detect language from file extension."""
        ext = Path(filename).suffix.lower()
        return self._extension_map.get(ext)

    def detect_from_shebang(self, code: str) -> Optional[str]:
        """Detect language from shebang line."""
        first_line = code.split("\n")[0].strip()
        if not first_line.startswith("#!"):
            return None
        
        # Extract interpreter name
        shebang_path = first_line[2:].strip()
        
        # Handle env-style shebangs: #!/usr/bin/env python
        if "env " in shebang_path:
            # Extract the argument after env
            env_parts = shebang_path.split("env ", 1)
            if len(env_parts) > 1:
                interpreter = env_parts[1].split()[0]  # Get first argument
            else:
                interpreter = ""
        else:
            # Regular shebang: #!/usr/bin/python
            parts = shebang_path.split("/")
            interpreter = parts[-1] if parts else ""
        
        # Remove version suffix (python3.11 -> python3)
        interpreter = re.sub(r"\d+\.\d+$", "", interpreter)
        interpreter = re.sub(r"\d+$", "", interpreter)
        
        return self._shebang_map.get(interpreter)

    def detect_from_patterns(self, code: str) -> Optional[str]:
        """Detect language from code patterns."""
        scores: Dict[str, int] = {}
        
        for lang, config in self.LANGUAGES.items():
            score = 0
            for pattern in config["patterns"]:
                if re.search(pattern, code, re.MULTILINE):
                    score += 1
            if score > 0:
                scores[lang] = score
        
        if not scores:
            return None
        
        return max(scores, key=scores.get)

    def detect(self, code: str, filename: Optional[str] = None) -> Tuple[str, float]:
        """
        Detect language from code with confidence score.
        
        Returns:
            Tuple of (language_name, confidence_score)
        """
        candidates: List[Tuple[str, float]] = []
        
        # Check extension first (highest confidence)
        if filename:
            lang = self.detect_from_extension(filename)
            if lang:
                candidates.append((lang, 0.95))
        
        # Check shebang (high confidence)
        lang = self.detect_from_shebang(code)
        if lang:
            candidates.append((lang, 0.90))
        
        # Check patterns (medium confidence)
        lang = self.detect_from_patterns(code)
        if lang:
            candidates.append((lang, 0.70))
        
        if not candidates:
            return ("text", 0.0)
        
        # Return highest confidence result
        return max(candidates, key=lambda x: x[1])

    def get_comment_style(self, language: str) -> str:
        """Get the comment style for a language."""
        config = self.LANGUAGES.get(language, {})
        return config.get("comment", "#")

    def get_extensions(self, language: str) -> List[str]:
        """Get supported extensions for a language."""
        config = self.LANGUAGES.get(language, {})
        return config.get("extensions", [])

    def list_languages(self) -> List[str]:
        """List all supported languages."""
        return list(self.LANGUAGES.keys())
