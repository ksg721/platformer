"""The pause menu shown over the active climb."""

import arcade


class PauseScreen:
    """Draw and control the in-game pause menu."""

    def __init__(self, screen_width, screen_height):
        """Create a pause menu sized for the virtual game window."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        self.mouse_x = screen_width / 2
        self.mouse_y = screen_height / 2

        center_x = screen_width / 2
        self.title_text = arcade.Text(
            "PAUSED",
            center_x,
            screen_height / 2 + 112,
            (255, 238, 177),
            26,
            anchor_x="center",
            bold=True,
        )
        self.subtitle_text = arcade.Text(
            "THE CLIMB IS WAITING",
            center_x,
            screen_height / 2 + 82,
            (143, 211, 191),
            9,
            anchor_x="center",
            bold=True,
        )
        self.restart_text = arcade.Text(
            "RESTART RUN",
            center_x,
            screen_height / 2 + 30,
            (20, 30, 50),
            11,
            anchor_x="center",
            bold=True,
        )
        self.settings_text = arcade.Text(
            "SETTINGS",
            center_x,
            screen_height / 2 - 28,
            (20, 30, 50),
            11,
            anchor_x="center",
            bold=True,
        )
        self.title_button_text = arcade.Text(
            "EXIT TO TITLE",
            center_x,
            screen_height / 2 - 86,
            (20, 30, 50),
            11,
            anchor_x="center",
            bold=True,
        )
        self.hint_text = arcade.Text(
            "ESC OR B  RESUME",
            center_x,
            screen_height / 2 - 135,
            (190, 216, 207),
            9,
            anchor_x="center",
        )

    @property
    def panel_left(self):
        """Return the left edge of the pause panel."""
        return self.screen_width / 2 - 210

    @property
    def panel_bottom(self):
        """Return the bottom edge of the pause panel."""
        return self.screen_height / 2 - 175

    @property
    def panel_width(self):
        """Return the pause panel width."""
        return 420

    @property
    def panel_height(self):
        """Return the pause panel height."""
        return 350

    @staticmethod
    def button_width():
        """Return the width shared by pause buttons."""
        return 240

    @staticmethod
    def button_height():
        """Return the height shared by pause buttons."""
        return 42

    @property
    def button_left(self):
        """Return the left edge shared by pause buttons."""
        return self.screen_width / 2 - self.button_width() / 2

    @property
    def restart_button_bottom(self):
        """Return the bottom edge of the restart button."""
        return self.screen_height / 2 + 8

    @property
    def settings_button_bottom(self):
        """Return the bottom edge of the settings button."""
        return self.screen_height / 2 - 50

    @property
    def title_button_bottom(self):
        """Return the bottom edge of the title button."""
        return self.screen_height / 2 - 108

    def show(self):
        """Make the pause menu visible."""
        self.visible = True

    def hide(self):
        """Hide the pause menu."""
        self.visible = False

    def set_mouse_position(self, x, y):
        """Remember the cursor position for hover feedback."""
        self.mouse_x = x
        self.mouse_y = y

    def _button_contains(self, bottom, x, y):
        """Return whether a point is inside a pause button."""
        return (
            self.button_left <= x <= self.button_left + self.button_width()
            and bottom <= y <= bottom + self.button_height()
        )

    def restart_button_contains(self, x, y):
        """Return whether a point is inside the restart button."""
        return self._button_contains(self.restart_button_bottom, x, y)

    def settings_button_contains(self, x, y):
        """Return whether a point is inside the settings button."""
        return self._button_contains(self.settings_button_bottom, x, y)

    def title_button_contains(self, x, y):
        """Return whether a point is inside the title button."""
        return self._button_contains(self.title_button_bottom, x, y)

    def draw(self):
        """Draw the pause overlay above the game world."""
        if not self.visible:
            return

        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.screen_width,
            self.screen_height,
            (4, 9, 18, 210),
        )

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

        self._draw_button(
            self.restart_button_bottom,
            self.restart_button_contains(self.mouse_x, self.mouse_y),
        )
        self._draw_button(
            self.settings_button_bottom,
            self.settings_button_contains(self.mouse_x, self.mouse_y),
        )
        self._draw_button(
            self.title_button_bottom,
            self.title_button_contains(self.mouse_x, self.mouse_y),
        )

        self.title_text.draw()
        self.subtitle_text.draw()
        self.restart_text.draw()
        self.settings_text.draw()
        self.title_button_text.draw()
        self.hint_text.draw()

    def _draw_button(self, bottom, hovered):
        """Draw one pause action button with a small shadow."""
        button_color = (255, 224, 137) if hovered else (143, 211, 191)
        arcade.draw_lbwh_rectangle_filled(
            self.button_left + 4,
            bottom - 4,
            self.button_width(),
            self.button_height(),
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.button_left,
            bottom,
            self.button_width(),
            self.button_height(),
            button_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.button_left,
            bottom,
            self.button_width(),
            self.button_height(),
            (255, 241, 177),
            2,
        )
