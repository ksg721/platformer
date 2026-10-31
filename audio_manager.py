"""Music and sound-effect management for Vertical Ascent."""

import sys
from pathlib import Path

import arcade


class AudioManager:
    """Load audio once and provide safe controls for music and sound effects."""

    MUSIC_FILES = {
        "menu": "menu_theme.wav",
        "gameplay": "climb_theme.wav",
    }
    EFFECT_FILES = {
        "land": "land.wav",
        "wall_hit": "wall_hit.wav",
        "menu_click": "menu_click.wav",
        "summit": "summit_fanfare.wav",
    }

    def __init__(self):
        """Load the small collection of game sounds from the audio folder."""
        self.music_enabled = True
        self.sound_effects_enabled = True
        self.music_volume = 0.32
        self.sound_effect_volume = 0.58
        self.requested_music = None
        self.current_music = None
        self.music_player = None

        self.music_sounds = {
            name: self._load_sound(filename)
            for name, filename in self.MUSIC_FILES.items()
        }
        self.effect_sounds = {
            name: self._load_sound(filename)
            for name, filename in self.EFFECT_FILES.items()
        }

    @staticmethod
    def _asset_path(filename):
        """Return a path that works in source form and in a PyInstaller build."""
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent
        return base_path / "assets" / "audio" / filename

    @classmethod
    def _load_sound(cls, filename):
        """Load one sound, returning None when an optional asset is unavailable."""
        path = cls._asset_path(filename)
        try:
            return arcade.load_sound(str(path))
        except (OSError, RuntimeError, ValueError):
            return None

    def apply_settings(self, music_enabled, sound_effects_enabled):
        """Apply the two audio preferences immediately."""
        self.music_enabled = bool(music_enabled)
        self.sound_effects_enabled = bool(sound_effects_enabled)

        if not self.music_enabled:
            self._stop_current_music()
        elif self.requested_music and self.music_player is None:
            self._start_requested_music()

    def play_music(self, track_name):
        """Request a looping music track and replace the current track if needed."""
        if track_name not in self.music_sounds:
            return

        self.requested_music = track_name
        if not self.music_enabled:
            self._stop_current_music()
            return

        if self.current_music == track_name and self.music_player is not None:
            return

        self._stop_current_music()
        self._start_requested_music()

    def _start_requested_music(self):
        """Start the requested music track when it loaded successfully."""
        if not self.music_enabled or not self.requested_music:
            return

        sound = self.music_sounds.get(self.requested_music)
        if sound is None:
            return

        try:
            self.music_player = arcade.play_sound(
                sound,
                volume=self.music_volume,
                loop=True,
            )
            self.current_music = self.requested_music
        except (OSError, RuntimeError, ValueError):
            self.music_player = None
            self.current_music = None

    def _stop_current_music(self):
        """Stop the active music player without clearing the requested track."""
        if self.music_player is not None:
            try:
                arcade.stop_sound(self.music_player)
            except (OSError, RuntimeError, ValueError):
                pass
        self.music_player = None
        self.current_music = None

    def pause_music(self):
        """Pause the current track while the pause menu is open."""
        if self.music_player is not None:
            try:
                self.music_player.pause()
            except (AttributeError, OSError, RuntimeError, ValueError):
                pass

    def resume_music(self):
        """Resume the current track after leaving the pause menu."""
        if self.music_player is not None:
            try:
                self.music_player.play()
            except (AttributeError, OSError, RuntimeError, ValueError):
                pass
        elif self.music_enabled:
            self._start_requested_music()

    def stop_music(self):
        """Stop the current track while keeping its requested context."""
        self._stop_current_music()

    def play_effect(self, effect_name):
        """Play a short sound effect when sound effects are enabled."""
        if not self.sound_effects_enabled:
            return None

        sound = self.effect_sounds.get(effect_name)
        if sound is None:
            return None

        try:
            return arcade.play_sound(sound, volume=self.sound_effect_volume)
        except (OSError, RuntimeError, ValueError):
            return None
