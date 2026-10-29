"""The title screen shown before the climb begins."""

import arcade


class StartScreen:
    """Draw and control the game's title screen."""

    def __init__(self, screen_width, screen_height):
        """Create a start screen sized for the game window."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = True
        self.mouse_x = screen_width / 2
        self.mouse_y = screen_height / 2

        center_x = screen_width / 2
        self.eyebrow_text = arcade.Text(
            "THE SUMMIT AWAITS",
            center_x,
            screen_height / 2 + 150,
            (143, 211, 191),
            9,
            anchor_x="center",
            bold=True,
        )
        self.title_text = arcade.Text(
            "VERTICAL ASCENT",
            center_x,
            screen_height / 2 + 102,
            (255, 238, 177),
            28,
            anchor_x="center",
            bold=True,
        )
        self.subtitle_text = arcade.Text(
            "A precision platforming climb",
            center_x,
            screen_height / 2 + 64,
            (207, 230, 218),
            12,
            anchor_x="center",
        )
        self.button_text = arcade.Text(
            "START CLIMB",
            center_x,
            screen_height / 2 - 30,
            (20, 30, 50),
            13,
            anchor_x="center",
            bold=True,
        )
        self.leaderboard_text = arcade.Text(
            "LEADERBOARD",
            center_x,
            screen_height / 2 - 105,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self.settings_text = arcade.Text(
            "SETTINGS",
            center_x,
            screen_height / 2 - 170,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self.quit_text = arcade.Text(
            "QUIT",
            center_x,
            screen_height / 2 - 215,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self.controls_text = arcade.Text(
            "A/D OR ARROWS MOVE    AIM + CHARGE WITH LEFT CLICK",
            center_x,
            screen_height / 2 - 275,
            (190, 216, 207),
            9,
            anchor_x="center",
        )

    @property
    def button_left(self):
        """Return the left edge of the start button."""
        return self.screen_width / 2 - 120

    @property
    def button_bottom(self):
        """Return the bottom edge of the start button."""
        return self.screen_height / 2 - 55

    @property
    def button_width(self):
        """Return the width of the start button."""
        return 240

    @property
    def button_height(self):
        """Return the height of the start button."""
        return 58

    @property
    def leaderboard_button_left(self):
        """Return the left edge of the leaderboard button."""
        return self.screen_width / 2 - 100

    @property
    def leaderboard_button_bottom(self):
        """Return the bottom edge of the leaderboard button."""
        return self.screen_height / 2 - 130

    @property
    def leaderboard_button_width(self):
        """Return the leaderboard button width."""
        return 200

    @property
    def leaderboard_button_height(self):
        """Return the leaderboard button height."""
        return 40

    @property
    def settings_button_left(self):
        """Return the left edge of the settings button."""
        return self.screen_width / 2 - 100

    @property
    def settings_button_bottom(self):
        """Return the bottom edge of the settings button."""
        return self.screen_height / 2 - 195

    @property
    def settings_button_width(self):
        """Return the settings button width."""
        return 200

    @property
    def settings_button_height(self):
        """Return the settings button height."""
        return 40

    @property
    def quit_button_left(self):
        """Return the left edge of the quit button."""
        return self.screen_width / 2 - 100

    @property
    def quit_button_bottom(self):
        """Return the bottom edge of the quit button."""
        return self.screen_height / 2 - 240

    @property
    def quit_button_width(self):
        """Return the quit button width."""
        return 200

    @property
    def quit_button_height(self):
        """Return the quit button height."""
        return 40

    def show(self):
        """Make the title screen visible."""
        self.visible = True

    def hide(self):
        """Hide the title screen."""
        self.visible = False

    def set_mouse_position(self, x, y):
        """Remember the cursor position for button hover feedback."""
        self.mouse_x = x
        self.mouse_y = y

    def button_contains(self, x, y):
        """Return whether a screen-space point is inside the start button."""
        return (
            self.button_left <= x <= self.button_left + self.button_width
            and self.button_bottom <= y <= self.button_bottom + self.button_height
        )

    def leaderboard_button_contains(self, x, y):
        """Return whether a screen-space point is inside the leaderboard button."""
        return (
            self.leaderboard_button_left <= x
            <= self.leaderboard_button_left + self.leaderboard_button_width
            and self.leaderboard_button_bottom
            <= y
            <= self.leaderboard_button_bottom + self.leaderboard_button_height
        )

    def settings_button_contains(self, x, y):
        """Return whether a screen-space point is inside the settings button."""
        return (
            self.settings_button_left <= x
            <= self.settings_button_left + self.settings_button_width
            and self.settings_button_bottom
            <= y
            <= self.settings_button_bottom + self.settings_button_height
        )

    def quit_button_contains(self, x, y):
        """Return whether a screen-space point is inside the quit button."""
        return (
            self.quit_button_left <= x
            <= self.quit_button_left + self.quit_button_width
            and self.quit_button_bottom
            <= y
            <= self.quit_button_bottom + self.quit_button_height
        )

    def draw(self):
        """Draw a self-contained title screen and start button."""
        if not self.visible:
            return

        self._draw_background()

        panel_width = 560
        panel_height = 480
        panel_left = (self.screen_width - panel_width) / 2
        panel_bottom = (self.screen_height - panel_height) / 2

        # A small shadow separates the panel from the dark background.
        arcade.draw_lbwh_rectangle_filled(
            panel_left + 8,
            panel_bottom - 8,
            panel_width,
            panel_height,
            (3, 8, 18),
        )
        arcade.draw_lbwh_rectangle_filled(
            panel_left,
            panel_bottom,
            panel_width,
            panel_height,
            (19, 31, 51),
        )
        arcade.draw_lbwh_rectangle_outline(
            panel_left,
            panel_bottom,
            panel_width,
            panel_height,
            (143, 211, 191),
            2,
        )
        arcade.draw_lbwh_rectangle_outline(
            panel_left + 8,
            panel_bottom + 8,
            panel_width - 16,
            panel_height - 16,
            (46, 74, 87),
            1,
        )

        self._draw_panel_accents(panel_left, panel_bottom, panel_width, panel_height)

        button_hovered = self.button_contains(self.mouse_x, self.mouse_y)
        button_color = (255, 224, 137) if button_hovered else (143, 211, 191)

        # The offset rectangle gives the button a little physical depth.
        arcade.draw_lbwh_rectangle_filled(
            self.button_left + 4,
            self.button_bottom - 4,
            self.button_width,
            self.button_height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.button_left,
            self.button_bottom,
            self.button_width,
            self.button_height,
            button_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.button_left,
            self.button_bottom,
            self.button_width,
            self.button_height,
            (255, 241, 177),
            2,
        )

        leaderboard_hovered = self.leaderboard_button_contains(
            self.mouse_x,
            self.mouse_y,
        )
        leaderboard_color = (
            (255, 224, 137) if leaderboard_hovered else (143, 211, 191)
        )
        arcade.draw_lbwh_rectangle_filled(
            self.leaderboard_button_left + 4,
            self.leaderboard_button_bottom - 4,
            self.leaderboard_button_width,
            self.leaderboard_button_height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.leaderboard_button_left,
            self.leaderboard_button_bottom,
            self.leaderboard_button_width,
            self.leaderboard_button_height,
            leaderboard_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.leaderboard_button_left,
            self.leaderboard_button_bottom,
            self.leaderboard_button_width,
            self.leaderboard_button_height,
            (255, 241, 177),
            2,
        )

        settings_hovered = self.settings_button_contains(
            self.mouse_x,
            self.mouse_y,
        )
        settings_color = (
            (255, 224, 137) if settings_hovered else (143, 211, 191)
        )
        arcade.draw_lbwh_rectangle_filled(
            self.settings_button_left + 4,
            self.settings_button_bottom - 4,
            self.settings_button_width,
            self.settings_button_height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.settings_button_left,
            self.settings_button_bottom,
            self.settings_button_width,
            self.settings_button_height,
            settings_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.settings_button_left,
            self.settings_button_bottom,
            self.settings_button_width,
            self.settings_button_height,
            (255, 241, 177),
            2,
        )

        quit_hovered = self.quit_button_contains(self.mouse_x, self.mouse_y)
        quit_color = (255, 224, 137) if quit_hovered else (143, 211, 191)
        arcade.draw_lbwh_rectangle_filled(
            self.quit_button_left + 4,
            self.quit_button_bottom - 4,
            self.quit_button_width,
            self.quit_button_height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.quit_button_left,
            self.quit_button_bottom,
            self.quit_button_width,
            self.quit_button_height,
            quit_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.quit_button_left,
            self.quit_button_bottom,
            self.quit_button_width,
            self.quit_button_height,
            (255, 241, 177),
            2,
        )

        self.eyebrow_text.draw()
        self.title_text.draw()
        self.subtitle_text.draw()
        self.button_text.draw()
        self.leaderboard_text.draw()
        self.settings_text.draw()
        self.quit_text.draw()
        self.controls_text.draw()

    def _draw_background(self):
        """Draw an opaque background so gameplay cannot show through."""
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.screen_width,
            self.screen_height,
            (7, 14, 28),
        )

        # Broad bands create depth without requiring image assets.
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

        # Subtle lines suggest the vertical structure of the climb.
        center_x = self.screen_width / 2
        for offset in (250, 270, 290):
            arcade.draw_line(
                center_x - offset,
                0,
                center_x - offset + 28,
                self.screen_height,
                (14, 35, 52),
                1,
            )
            arcade.draw_line(
                center_x + offset,
                0,
                center_x + offset - 28,
                self.screen_height,
                (14, 35, 52),
                1,
            )

        # Narrow side rails frame the screen and reinforce the game's theme.
        arcade.draw_lbwh_rectangle_filled(
            42,
            42,
            3,
            self.screen_height - 84,
            (46, 91, 92),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.screen_width - 45,
            42,
            3,
            self.screen_height - 84,
            (46, 91, 92),
        )

    @staticmethod
    def _draw_panel_accents(panel_left, panel_bottom, panel_width, panel_height):
        """Draw small corner accents around the title panel."""
        accent_color = (255, 224, 137)
        accent_length = 30
        accent_thickness = 3
        inset = 1

        for x in (panel_left, panel_left + panel_width - accent_length):
            arcade.draw_lbwh_rectangle_filled(
                x,
                panel_bottom + inset,
                accent_length,
                accent_thickness,
                accent_color,
            )
            arcade.draw_lbwh_rectangle_filled(
                x,
                panel_bottom + panel_height - inset - accent_thickness,
                accent_length,
                accent_thickness,
                accent_color,
            )
