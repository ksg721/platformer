"""The final summit screen shown after the player completes the climb."""

import arcade


class WinScreen:
    """Draw and control the game's completion overlay."""

    def __init__(self, screen_width, screen_height):
        """Create a win screen sized for the game window."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        self.mouse_x = screen_width / 2
        self.mouse_y = screen_height / 2
        self.name_input = ""
        self.score_saved = False

        center_x = screen_width / 2
        self.title_text = arcade.Text(
            "ASCENT COMPLETE",
            center_x,
            screen_height / 2 + 104,
            (255, 224, 137),
            24,
            anchor_x="center",
            bold=True,
        )
        self.subtitle_text = arcade.Text(
            "You reached the summit.",
            center_x,
            screen_height / 2 + 70,
            (226, 246, 223),
            12,
            anchor_x="center",
        )
        self.stats_text = arcade.Text(
            "TIME 00:00    JUMPS 000",
            center_x,
            screen_height / 2 + 37,
            (226, 246, 223),
            11,
            anchor_x="center",
            bold=True,
        )
        self.name_label_text = arcade.Text(
            "ENTER YOUR NAME",
            center_x,
            screen_height / 2 + 3,
            (143, 211, 191),
            9,
            anchor_x="center",
            bold=True,
        )
        self.name_text = arcade.Text(
            "TYPE YOUR NAME",
            center_x,
            screen_height / 2 - 29,
            (20, 30, 50),
            12,
            anchor_x="center",
            bold=True,
        )
        self.save_button_text = arcade.Text(
            "SAVE SCORE",
            center_x,
            screen_height / 2 - 88,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self.prompt_text = arcade.Text(
            "TYPE A NAME, THEN PRESS ENTER OR CLICK SAVE",
            center_x,
            screen_height / 2 - 137,
            (190, 216, 207),
            9,
            anchor_x="center",
        )

    def show(self, elapsed_seconds=0, jump_count=0):
        """Make the completion overlay visible with final run statistics."""
        total_seconds = max(0, int(elapsed_seconds))
        minutes, seconds = divmod(total_seconds, 60)
        self.stats_text.text = (
            f"TIME {minutes:02d}:{seconds:02d}    JUMPS {jump_count:03d}"
        )
        self.name_input = ""
        self.score_saved = False
        self.name_text.text = "TYPE YOUR NAME"
        self.save_button_text.text = "SAVE SCORE"
        self.prompt_text.text = "TYPE A NAME, THEN PRESS ENTER OR CLICK SAVE"
        self.prompt_text.color = (190, 216, 207)
        self.visible = True

    def hide(self):
        """Hide the completion overlay."""
        self.visible = False

    def set_mouse_position(self, x, y):
        """Remember the cursor position for button hover feedback."""
        self.mouse_x = x
        self.mouse_y = y

    def handle_text(self, text):
        """Append safe, readable characters to the player's name."""
        if not self.visible or self.score_saved:
            return

        for character in text:
            if character.isalnum() or character in " -_":
                if len(self.name_input) < 12:
                    self.name_input += character
        self._update_name_text()

    def handle_backspace(self):
        """Remove the last character from the name field."""
        if not self.visible or self.score_saved:
            return
        self.name_input = self.name_input[:-1]
        self._update_name_text()

    def mark_saved(self):
        """Switch the screen from name entry to the saved-score state."""
        self.score_saved = True
        self.save_button_text.text = "VIEW LEADERBOARD"
        self.prompt_text.text = "SCORE SAVED  •  PRESS L OR VIEW LEADERBOARD"
        self.prompt_text.color = (245, 197, 103)

    def show_save_error(self):
        """Tell the player that a name is required before saving."""
        self.prompt_text.text = "NAME REQUIRED  •  TYPE A NAME FIRST"
        self.prompt_text.color = (255, 157, 126)

    def show_save_failure(self):
        """Tell the player when the local leaderboard could not be written."""
        self.prompt_text.text = "COULD NOT SAVE SCORE  •  TRY AGAIN"
        self.prompt_text.color = (255, 157, 126)

    def save_button_contains(self, x, y):
        """Return whether a point is inside the save/action button."""
        return (
            self.save_button_left <= x <= self.save_button_left + self.save_button_width
            and self.save_button_bottom
            <= y
            <= self.save_button_bottom + self.save_button_height
        )

    @property
    def save_button_left(self):
        """Return the left edge of the save/action button."""
        return self.screen_width / 2 - 100

    @property
    def save_button_bottom(self):
        """Return the bottom edge of the save/action button."""
        return self.screen_height / 2 - 108

    @property
    def save_button_width(self):
        """Return the save/action button width."""
        return 200

    @property
    def save_button_height(self):
        """Return the save/action button height."""
        return 42

    def _update_name_text(self):
        """Refresh the visible name field after text input."""
        self.name_text.text = self.name_input or "TYPE YOUR NAME"

    def draw(self):
        """Draw the dimmed summit scene and completion message."""
        if not self.visible:
            return

        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.screen_width,
            self.screen_height,
            (7, 12, 28, 185),
        )

        panel_width = 500
        panel_height = 340
        panel_left = (self.screen_width - panel_width) / 2
        panel_bottom = (self.screen_height - panel_height) / 2

        arcade.draw_lbwh_rectangle_filled(
            panel_left,
            panel_bottom,
            panel_width,
            panel_height,
            (20, 30, 50, 238),
        )
        arcade.draw_lbwh_rectangle_outline(
            panel_left,
            panel_bottom,
            panel_width,
            panel_height,
            (143, 211, 191),
            2,
        )

        name_box_left = self.screen_width / 2 - 160
        name_box_bottom = self.screen_height / 2 - 52
        name_box_width = 320
        name_box_height = 40
        arcade.draw_lbwh_rectangle_filled(
            name_box_left,
            name_box_bottom,
            name_box_width,
            name_box_height,
            (226, 238, 229),
        )
        arcade.draw_lbwh_rectangle_outline(
            name_box_left,
            name_box_bottom,
            name_box_width,
            name_box_height,
            (143, 211, 191),
            2,
        )

        button_hovered = self.save_button_contains(self.mouse_x, self.mouse_y)
        button_color = (255, 224, 137) if button_hovered else (143, 211, 191)
        arcade.draw_lbwh_rectangle_filled(
            self.save_button_left + 4,
            self.save_button_bottom - 4,
            self.save_button_width,
            self.save_button_height,
            (7, 15, 27),
        )
        arcade.draw_lbwh_rectangle_filled(
            self.save_button_left,
            self.save_button_bottom,
            self.save_button_width,
            self.save_button_height,
            button_color,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.save_button_left,
            self.save_button_bottom,
            self.save_button_width,
            self.save_button_height,
            (255, 241, 177),
            2,
        )

        beacon_x = self.screen_width / 2
        beacon_y = panel_bottom + panel_height - 28
        arcade.draw_circle_filled(
            beacon_x,
            beacon_y,
            24,
            (245, 197, 103, 28),
        )
        arcade.draw_circle_filled(
            beacon_x,
            beacon_y,
            7,
            (255, 224, 137),
        )
        arcade.draw_line(
            beacon_x - 13,
            beacon_y,
            beacon_x + 13,
            beacon_y,
            (255, 241, 177),
            1,
        )

        self.title_text.draw()
        self.subtitle_text.draw()
        self.stats_text.draw()
        self.name_label_text.draw()
        self.name_text.draw()
        self.save_button_text.draw()
        self.prompt_text.draw()
