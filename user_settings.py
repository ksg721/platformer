"""Persistent player preferences for Vertical Ascent."""

import json
import os
from pathlib import Path


class SettingsStore:
    """Load, validate, and save preferences in the user's app-data folder."""

    DEFAULTS = {
        "fullscreen": False,
        "mouse_sensitivity": 1.0,
        "invert_mouse": False,
        "show_hud": True,
        "show_power_bar": True,
        "reduced_effects": False,
        "reduced_camera_motion": False,
        "show_control_hints": True,
    }

    SENSITIVITY_VALUES = (0.75, 1.0, 1.25)

    def __init__(self, file_path=None):
        """Create a settings store, using a stable path by default."""
        self.file_path = Path(file_path) if file_path else self.default_file_path()
        self.values = self.load()

    @staticmethod
    def default_file_path():
        """Return a user-writable path that works for the packaged game."""
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            base_directory = Path(local_app_data)
        else:
            base_directory = Path.home() / "AppData" / "Local"
        return base_directory / "VerticalAscent" / "settings.json"

    def load(self):
        """Load saved values and fall back safely when the file is missing."""
        values = dict(self.DEFAULTS)
        try:
            saved_values = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return values

        if not isinstance(saved_values, dict):
            return values

        for key, default_value in self.DEFAULTS.items():
            if key not in saved_values:
                continue

            saved_value = saved_values[key]
            if isinstance(default_value, bool):
                if isinstance(saved_value, bool):
                    values[key] = saved_value
            elif key == "mouse_sensitivity":
                try:
                    sensitivity = float(saved_value)
                except (TypeError, ValueError):
                    continue
                if sensitivity in self.SENSITIVITY_VALUES:
                    values[key] = sensitivity

        return values

    def save(self):
        """Write the current preferences and report whether it succeeded."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(
                json.dumps(self.values, indent=2),
                encoding="utf-8",
            )
        except OSError:
            return False
        return True

    def get(self, key):
        """Return one preference value."""
        return self.values[key]

    def set(self, key, value):
        """Set one known preference and save it immediately."""
        if key not in self.DEFAULTS:
            return False
        self.values[key] = value
        return self.save()

    def reset(self):
        """Restore every preference to its default value."""
        self.values = dict(self.DEFAULTS)
        return self.save()
