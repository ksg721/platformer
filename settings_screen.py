"""The settings menu shown from the title screen."""

import arcade

from user_settings import SettingsStore


class SettingsScreen:
    """Draw and edit the player's saved preferences."""

    ROWS = (
        ("fullscreen", "DISPLAY MODE"),
        ("mouse_sensitivity", "MOUSE AIM SENSITIVITY"),
        ("invert_mouse", "INVERT VERTICAL AIM"),
        ("show_hud", "SHOW HUD STATISTICS"),
        ("show_power_bar", "SHOW JUMP POWER BAR"),
        ("reduced_effects", "REDUCED VISUAL EFFECTS"),
        ("reduced_camera_motion", "REDUCED CAMERA MOTION"),
        ("show_control_hints", "SHOW CONTROL HINTS"),
    )

    def __init__(self, screen_width, screen_height, settings_store):
        """Create a settings screen backed by a persistent store."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.store = settings_store
        self.visible = False
        self.mouse_x = screen_width / 2
        self.mouse_y = screen_height / 2
        self.reset_confirmation = False
        self.message = ""

        center_x = screen_width / 2
        self.title_text = arcade.Text(
            "SETTINGS",
            center_x,
            screen_height - 66,
            (255, 238, 177),
            25,
            anchor_x="center",
            bold=True,
        )
        self.subtitle_text = arcade.Text(
            "MAKE THE CLIMB YOUR OWN",
            center_x,
            screen_height - 94,
            (143, 211, 191),
            9,
            anchor_x="center",
            bold=True,
        )
        self.row_labels = []
        self.row_values = []
        for row_index, (_, label) in enumerate(self.ROWS):
            row_y = self.row_bottom(row_index) + 11
            self.row_labels.append(
                arcade.Text(label, 125, row_y, (226, 246, 223), 10, bold=True)
            )
            self.row_values.append(
                arcade.Text(
                    "",
                    675,
                    row_y,
                    (255, 224, 137),
                    10,
                    anchor_x="right",
                    bold=True,
                )
            )

        self.message_text = arcade.Text(
            "",
            center_x,
            112,
            (245, 197, 103),
            9,
            anchor_x="center",
            bold=True,
        )
        self.hint_text = arcade.Text(
            "CLICK A SETTING TO CHANGE IT     ESC OR B TO RETURN",
            center_x,
            25,
            (190, 216, 207),
            9,
            anchor_x="center",
        )
        self.reset_leaderboard_text = arcade.Text(
            "RESET LEADERBOARD",
            190,
            65,
            (20, 30, 50),
            9,
            anchor_x="center",
            bold=True,
        )
        self.reset_defaults_text = arcade.Text(
            "RESET DEFAULTS",
            400,
            65,
            (20, 30, 50),
            9,
            anchor_x="center",
            bold=True,
        )
        self.back_text = arcade.Text(
            "BACK",
            610,
            65,
            (20, 30, 50),
            9,
            anchor_x="center",
            bold=True,
        )

    @property
    def panel_left(self):
        """Return the left edge of the settings panel."""
        return 50

    @property
    def panel_bottom(self):
        """Return the bottom edge of the settings panel."""
        return 25

    @property
    def panel_width(self):
        """Return the settings panel width."""
        return self.screen_width - 100

    @property
    def panel_height(self):
        """Return the settings panel height."""
        return self.screen_height - 50

    @staticmethod
    def row_bottom(row_index):
        """Return the bottom edge of one settings row."""
        return 442 - row_index * 40

    @staticmethod
    def row_height():
        """Return the height of one settings row."""
        return 34

    def show(self):
        """Make the settings screen visible."""
        self.visible = True
        self.reset_confirmation = False
        self.message = ""

    def hide(self):
        """Hide the settings screen."""
        self.visible = False

    def set_mouse_position(self, x, y):
        """Remember the cursor position for hover feedback."""
        self.mouse_x = x
        self.mouse_y = y

    def row_contains(self, row_index, x, y):
        """Return whether a point is inside a setting row."""
        return (
            95 <= x <= 705
            and self.row_bottom(row_index)
            <= y
            <= self.row_bottom(row_index) + self.row_height()
        )

    def row_at(self, x, y):
        """Return the row index beneath a point, or None."""
        for row_index in range(len(self.ROWS)):
            if self.row_contains(row_index, x, y):
                return row_index
        return None

    def activate_row(self, row_index):
        """Cycle or toggle one setting and persist the change."""
        key, _ = self.ROWS[row_index]
        if key == "mouse_sensitivity":
            current_value = self.store.get(key)
            current_index = SettingsStore.SENSITIVITY_VALUES.index(current_value)
            next_index = (current_index + 1) % len(SettingsStore.SENSITIVITY_VALUES)
            self.store.set(key, SettingsStore.SENSITIVITY_VALUES[next_index])
        else:
            self.store.set(key, not self.store.get(key))
        self.message = "SETTING SAVED"
        self.reset_confirmation = False

    def reset_leaderboard_button_contains(self, x, y):
        """Return whether a point is inside the leaderboard reset button."""
        return 95 <= x <= 285 and 48 <= y <= 84

    def reset_defaults_button_contains(self, x, y):
        """Return whether a point is inside the reset-defaults button."""
        return 305 <= x <= 495 and 48 <= y <= 84

    def back_button_contains(self, x, y):
        """Return whether a point is inside the Back button."""
        return 515 <= x <= 705 and 48 <= y <= 84

    def request_leaderboard_reset(self):
        """Request a second click before deleting saved scores."""
        if self.reset_confirmation:
            self.reset_confirmation = False
            self.message = "LEADERBOARD CLEARED"
            return True

        self.reset_confirmation = True
        self.message = "CLICK RESET LEADERBOARD AGAIN TO CONFIRM"
        return False

    def reset_defaults(self):
        """Restore default settings and show a confirmation message."""
        self.store.reset()
        self.reset_confirmation = False
        self.message = "DEFAULT SETTINGS RESTORED"

    def draw(self):
        """Draw the opaque settings screen."""
        if not self.visible:
            return

        self._draw_background()
        arcade.draw_lbwh_rectangle_filled(
            self.panel_left + 8,
            self.panel_bottom - 8,
            self.panel_width,
            self.panel_height,
            (3, 8, 18),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.panel_left,
            self.panel_bottom,
            self.panel_width,
            self.panel_height,
            (19, 31, 51),
        )
        arcade.draw_lbwh_rectangle_outline(
            self.panel_left,
            self.panel_bottom,
            self.panel_width,
            self.panel_height,
            (143, 211, 191),
            2,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.panel_left + 8,
            self.panel_bottom + 8,
            self.panel_width - 16,
            self.panel_height - 16,
            (46, 74, 87),
            1,
        )

        for row_index, (key, _) in enumerate(self.ROWS):
            row_bottom = self.row_bottom(row_index)
            hovered = self.row_contains(row_index, self.mouse_x, self.mouse_y)
            row_color = (32, 53, 72) if hovered else (25, 42, 61)
            arcade.draw_lbwh_rectangle_filled(
                95,
                row_bottom,
                610,
                self.row_height(),
                row_color,
            )
            arcade.draw_lbwh_rectangle_outline(
                95,
                row_bottom,
                610,
                self.row_height(),
                (46, 74, 87),
                1,
            )
            self.row_values[row_index].text = self.display_value(key)
            self.row_labels[row_index].draw()
            self.row_values[row_index].draw()

        self._draw_button(
            95,
            48,
            190,
            36,
            self.reset_leaderboard_button_contains(self.mouse_x, self.mouse_y),
        )
        self._draw_button(
            305,
            48,
            190,
            36,
            self.reset_defaults_button_contains(self.mouse_x, self.mouse_y),
        )
        self._draw_button(
            515,
            48,
            190,
            36,
            self.back_button_contains(self.mouse_x, self.mouse_y),
        )

        self.title_text.draw()
        self.subtitle_text.draw()
        self.reset_leaderboard_text.draw()
        self.reset_defaults_text.draw()
        self.back_text.draw()
        if self.message:
            self.message_text.text = self.message
            self.message_text.draw()
        else:
            self.hint_text.draw()

    def display_value(self, key):
        """Return the user-facing value for a setting key."""
        value = self.store.get(key)
        if key == "fullscreen":
            return "FULLSCREEN" if value else "WINDOWED"
        if key == "mouse_sensitivity":
            labels = {0.75: "LOW", 1.0: "NORMAL", 1.25: "HIGH"}
            return labels[value]
        if key in ("reduced_effects", "reduced_camera_motion"):
            return "REDUCED" if value else "FULL"
        return "ON" if value else "OFF"

    @staticmethod
    def _draw_button(left, bottom, width, height, hovered):
        """Draw a compact settings action button."""
        button_color = (255, 224, 137) if hovered else (143, 211, 191)
        arcade.draw_lbwh_rectangle_filled(
            left + 4,
            bottom - 4,
            width,
            height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(left, bottom, width, height, button_color)
        arcade.draw_lbwh_rectangle_outline(
            left,
            bottom,
            width,
            height,
            (255, 241, 177),
            2,
        )

    def _draw_background(self):
        """Draw an opaque background so the game cannot show through."""
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.screen_width,
            self.screen_height,
            (7, 14, 28),
        )
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.screen_width,
            self.screen_height * 0.34,
            (10, 24, 40),
        )
        arcade.draw_lbwh_rectangle_filled(
            0,
            self.screen_height * 0.34,
            self.screen_width,
            self.screen_height * 0.33,
            (9, 20, 36),
        )
