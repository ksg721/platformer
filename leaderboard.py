"""Persistent leaderboard storage for completed Vertical Ascent runs."""

import json
import os
from pathlib import Path


class LeaderboardStore:
    """Load and save the best completed runs on the local computer."""

    MAX_ENTRIES = 100
    DISPLAY_ENTRIES = 10

    def __init__(self, file_path=None):
        """Create a store, using a user-writable path by default."""
        self.file_path = Path(file_path) if file_path else self.default_file_path()

    @staticmethod
    def default_file_path():
        """Return a stable location that also works for a packaged .exe."""
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            base_directory = Path(local_app_data)
        else:
            base_directory = Path.home() / "AppData" / "Local"
        return base_directory / "VerticalAscent" / "leaderboard.json"

    def load(self):
        """Return valid saved entries, or an empty list when none exist."""
        try:
            saved_entries = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return []

        if not isinstance(saved_entries, list):
            return []

        entries = []
        for saved_entry in saved_entries:
            if not isinstance(saved_entry, dict):
                continue

            name = str(saved_entry.get("name", "PLAYER")).strip()[:12]
            if not name:
                name = "PLAYER"

            try:
                time_seconds = max(0, int(saved_entry.get("time_seconds", 0)))
                jump_count = max(0, int(saved_entry.get("jumps", 0)))
            except (TypeError, ValueError):
                continue

            entries.append(
                {
                    "name": name,
                    "time_seconds": time_seconds,
                    "jumps": jump_count,
                }
            )

        return entries

    def add_score(self, name, time_seconds, jump_count):
        """Save a completed run and return it, or None if saving fails."""
        clean_name = " ".join(str(name).strip().split())[:12] or "PLAYER"
        entry = {
            "name": clean_name,
            "time_seconds": max(0, int(time_seconds)),
            "jumps": max(0, int(jump_count)),
        }

        entries = self.load()
        entries.append(entry)
        entries = self.sorted_entries("time", entries)[: self.MAX_ENTRIES]

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(
                json.dumps(entries, indent=2),
                encoding="utf-8",
            )
        except OSError:
            return None

        return entry

    def clear(self):
        """Remove all saved scores and report whether the action succeeded."""
        try:
            if self.file_path.exists():
                self.file_path.unlink()
        except OSError:
            return False
        return True

    @staticmethod
    def sorted_entries(sort_mode="time", entries=None):
        """Return entries ordered by time or by the fewest jumps."""
        entries_to_sort = list(entries) if entries is not None else []

        if sort_mode == "jumps":
            sort_key = lambda entry: (
                entry["jumps"],
                entry["time_seconds"],
                entry["name"].lower(),
            )
        else:
            sort_key = lambda entry: (
                entry["time_seconds"],
                entry["jumps"],
                entry["name"].lower(),
            )

        return sorted(entries_to_sort, key=sort_key)

    def ranked_entries(self, sort_mode="time"):
        """Load and sort the saved entries for display."""
        return self.sorted_entries(sort_mode, self.load())[: self.MAX_ENTRIES]

    @staticmethod
    def format_time(time_seconds):
        """Format a number of seconds as minutes and seconds."""
        total_seconds = max(0, int(time_seconds))
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
