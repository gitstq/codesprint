"""
History management module for CodeSprint.

Manages execution history, favorites, and snippets storage.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class HistoryEntry:
    """A single history entry."""
    id: str
    code: str
    language: str
    filename: Optional[str]
    output: str
    error: str
    success: bool
    execution_time: float
    timestamp: str
    favorite: bool = False
    tags: List[str] = None

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


class HistoryManager:
    """Manages execution history and favorites."""

    def __init__(self, history_dir: Optional[str] = None) -> None:
        """
        Initialize history manager.
        
        Args:
            history_dir: Directory to store history files
        """
        if history_dir:
            self.history_dir = Path(history_dir)
        else:
            self.history_dir = Path.home() / ".codesprint" / "history"
        
        self.history_file = self.history_dir / "history.json"
        self.favorites_file = self.history_dir / "favorites.json"
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensure history directory exists."""
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def _generate_id(self) -> str:
        """Generate a unique ID for history entry."""
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    def add_entry(
        self,
        code: str,
        language: str,
        output: str,
        error: str,
        success: bool,
        execution_time: float,
        filename: Optional[str] = None,
    ) -> HistoryEntry:
        """
        Add a new history entry.
        
        Returns:
            The created HistoryEntry
        """
        entry = HistoryEntry(
            id=self._generate_id(),
            code=code,
            language=language,
            filename=filename,
            output=output,
            error=error,
            success=success,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
        )
        
        history = self.load_history()
        history.insert(0, entry)  # Most recent first
        
        # Keep only last 1000 entries
        if len(history) > 1000:
            history = history[:1000]
        
        self._save_history(history)
        return entry

    def load_history(self) -> List[HistoryEntry]:
        """Load history from file."""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [HistoryEntry(**item) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_history(self, history: List[HistoryEntry]) -> None:
        """Save history to file."""
        data = [asdict(entry) for entry in history]
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_entry(self, entry_id: str) -> Optional[HistoryEntry]:
        """Get a specific history entry by ID."""
        history = self.load_history()
        for entry in history:
            if entry.id == entry_id:
                return entry
        return None

    def delete_entry(self, entry_id: str) -> bool:
        """Delete a history entry."""
        history = self.load_history()
        new_history = [e for e in history if e.id != entry_id]
        if len(new_history) < len(history):
            self._save_history(new_history)
            return True
        return False

    def clear_history(self) -> None:
        """Clear all history."""
        self._save_history([])

    def toggle_favorite(self, entry_id: str) -> bool:
        """Toggle favorite status of an entry."""
        history = self.load_history()
        for entry in history:
            if entry.id == entry_id:
                entry.favorite = not entry.favorite
                self._save_history(history)
                return entry.favorite
        return False

    def get_favorites(self) -> List[HistoryEntry]:
        """Get all favorite entries."""
        history = self.load_history()
        return [e for e in history if e.favorite]

    def add_tag(self, entry_id: str, tag: str) -> bool:
        """Add a tag to an entry."""
        history = self.load_history()
        for entry in history:
            if entry.id == entry_id:
                if tag not in entry.tags:
                    entry.tags.append(tag)
                    self._save_history(history)
                return True
        return False

    def remove_tag(self, entry_id: str, tag: str) -> bool:
        """Remove a tag from an entry."""
        history = self.load_history()
        for entry in history:
            if entry.id == entry_id:
                if tag in entry.tags:
                    entry.tags.remove(tag)
                    self._save_history(history)
                return True
        return False

    def search(
        self,
        query: str,
        language: Optional[str] = None,
        success_only: bool = False,
    ) -> List[HistoryEntry]:
        """
        Search history entries.
        
        Args:
            query: Search query (searches in code and output)
            language: Filter by language
            success_only: Only return successful executions
            
        Returns:
            List of matching entries
        """
        history = self.load_history()
        query_lower = query.lower()
        results = []
        
        for entry in history:
            # Filter by language
            if language and entry.language != language:
                continue
            
            # Filter by success
            if success_only and not entry.success:
                continue
            
            # Search in code and output
            if (
                query_lower in entry.code.lower()
                or query_lower in entry.output.lower()
                or query_lower in entry.error.lower()
            ):
                results.append(entry)
        
        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get history statistics."""
        history = self.load_history()
        
        if not history:
            return {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "favorites": 0,
                "languages": {},
                "avg_execution_time": 0.0,
            }
        
        successful = sum(1 for e in history if e.success)
        languages: Dict[str, int] = {}
        total_time = 0.0
        
        for entry in history:
            languages[entry.language] = languages.get(entry.language, 0) + 1
            total_time += entry.execution_time
        
        return {
            "total": len(history),
            "successful": successful,
            "failed": len(history) - successful,
            "favorites": sum(1 for e in history if e.favorite),
            "languages": languages,
            "avg_execution_time": total_time / len(history),
        }

    def export_history(self, output_path: str, format: str = "json") -> None:
        """
        Export history to a file.
        
        Args:
            output_path: Path to export file
            format: Export format (json, markdown)
        """
        history = self.load_history()
        
        if format == "json":
            data = [asdict(entry) for entry in history]
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            lines = ["# CodeSprint History Export\n"]
            lines.append(f"Exported: {datetime.now().isoformat()}\n")
            lines.append(f"Total entries: {len(history)}\n\n")
            
            for entry in history:
                lines.append(f"## {entry.id}\n")
                lines.append(f"- Language: {entry.language}\n")
                lines.append(f"- Success: {entry.success}\n")
                lines.append(f"- Time: {entry.execution_time:.3f}s\n")
                lines.append(f"- Timestamp: {entry.timestamp}\n")
                lines.append(f"\n### Code\n```\n{entry.code}\n```\n")
                if entry.output:
                    lines.append(f"\n### Output\n```\n{entry.output}\n```\n")
                if entry.error:
                    lines.append(f"\n### Error\n```\n{entry.error}\n```\n")
                lines.append("\n---\n\n")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
