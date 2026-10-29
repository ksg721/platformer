"""The leaderboard screen shown from the title screen."""

import arcade

from leaderboard import LeaderboardStore


class LeaderboardScreen:
    """Draw and interact with saved completion times and jump counts."""

    def __init__(self, screen_width, screen_height, leaderboard_store):
        """Create a leaderboard screen backed by a persistent store."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.store = leaderboard_store
        self.visible = False
        self.sort_mode = "time"
        self.mouse_x = screen_width / 2
        self.mouse_y = screen_height / 2

        center_x = screen_width / 2
        self.title_text = arcade.Text(
            "LEADERBOARD",
            center_x,
            screen_height - 76,
            (255, 238, 177),
            25,
            anchor_x="center",
            bold=True,
        )
        self.subtitle_text = arcade.Text(
            "THE BEST CLIMBS TO THE SUMMIT",
            center_x,
            screen_height - 105,
            (143, 211, 191),
            9,
            anchor_x="center",
            bold=True,
        )
        self.sort_text = arcade.Text(
            "",
            center_x,
            screen_height - 142,
            (207, 230, 218),
            10,
            anchor_x="center",
            bold=True,
        )
        self.column_rank_text = arcade.Text(
            "RANK",
            142,
            screen_height - 178,
            (143, 211, 191),
            9,
            bold=True,
        )
        self.column_name_text = arcade.Text(
            "PLAYER",
            204,
            screen_height - 178,
            (143, 211, 191),
            9,
            bold=True,
        )
        self.column_time_text = arcade.Text(
            "TIME",
            548,
            screen_height - 178,
            (143, 211, 191),
            9,
            anchor_x="right",
            bold=True,
        )
        self.column_jumps_text = arcade.Text(
            "JUMPS",
            674,
            screen_height - 178,
            (143, 211, 191),
            9,
            anchor_x="right",
            bold=True,
        )

        self.rank_texts = []
        self.name_texts = []
        self.time_texts = []
        self.jumps_texts = []
        for row_index in range(LeaderboardStore.DISPLAY_ENTRIES):
            row_y = screen_height - 210 - row_index * 30
            self.rank_texts.append(arcade.Text("", 142, row_y, (226, 246, 223), 11))
            self.name_texts.append(arcade.Text("", 204, row_y, (226, 246, 223), 11))
            self.time_texts.append(
                arcade.Text(
                    "",
                    548,
                    row_y,
                    (255, 224, 137),
                    11,
                    anchor_x="right",
                )
            )
            self.jumps_texts.append(
                arcade.Text(
                    "",
                    674,
                    row_y,
                    (226, 246, 223),
                    11,
                    anchor_x="right",
                )
            )

        self.empty_text = arcade.Text(
            "NO COMPLETED CLIMBS YET",
            center_x,
            screen_height / 2,
            (190, 216, 207),
            12,
            anchor_x="center",
        )
        self.hint_text = arcade.Text(
            "T TO SWITCH SORT     ESC OR B TO RETURN",
            center_x,
            25,
            (190, 216, 207),
            9,
            anchor_x="center",
        )
        self.sort_button_text = arcade.Text(
            "SORT: TIME",
            205,
            67,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self.back_button_text = arcade.Text(
            "BACK",
            650,
            67,
            (20, 30, 50),
            10,
            anchor_x="center",
            bold=True,
        )
        self._update_sort_text()

    @property
    def panel_left(self):
        """Return the left edge of the leaderboard panel."""
        return (self.screen_width - 620) / 2

    @property
    def panel_bottom(self):
        """Return the bottom edge of the leaderboard panel."""
        return 45

    @property
    def panel_width(self):
        """Return the leaderboard panel width."""
        return 620

    @property
    def panel_height(self):
        """Return the leaderboard panel height."""
        return 510

    @property
    def sort_button_left(self):
        """Return the left edge of the sort button."""
        return 115

    @property
    def sort_button_bottom(self):
        """Return the bottom edge of the sort button."""
        return 48

    @property
    def sort_button_width(self):
        """Return the sort button width."""
        return 180

    @property
    def sort_button_height(self):
        """Return the sort button height."""
        return 38

    @property
    def back_button_left(self):
        """Return the left edge of the back button."""
        return 580

    @property
    def back_button_bottom(self):
        """Return the bottom edge of the back button."""
        return 48

    @property
    def back_button_width(self):
        """Return the back button width."""
        return 140

    @property
    def back_button_height(self):
        """Return the back button height."""
        return 38

    def show(self):
        """Make the leaderboard visible and refresh its entries."""
        self.visible = True

    def hide(self):
        """Hide the leaderboard."""
        self.visible = False

    def set_mouse_position(self, x, y):
        """Remember the cursor position for button hover feedback."""
        self.mouse_x = x
        self.mouse_y = y

    def toggle_sort(self):
        """Switch between the default time ranking and jump ranking."""
        self.sort_mode = "jumps" if self.sort_mode == "time" else "time"
        self._update_sort_text()

    def back_contains(self, x, y):
        """Return whether a point is inside the Back button."""
        return (
            self.back_button_left <= x <= self.back_button_left + self.back_button_width
            and self.back_button_bottom
            <= y
            <= self.back_button_bottom + self.back_button_height
        )

    def sort_contains(self, x, y):
        """Return whether a point is inside the sort button."""
        return (
            self.sort_button_left <= x <= self.sort_button_left + self.sort_button_width
            and self.sort_button_bottom
            <= y
            <= self.sort_button_bottom + self.sort_button_height
        )

    def draw(self):
        """Draw the opaque leaderboard screen."""
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

        arcade.draw_line(
            self.panel_left + 30,
            self.screen_height - 190,
            self.panel_left + self.panel_width - 30,
            self.screen_height - 190,
            (46, 74, 87),
            1,
        )

        entries = self.store.ranked_entries(self.sort_mode)[
            : LeaderboardStore.DISPLAY_ENTRIES
        ]
        if entries:
            for row_index, entry in enumerate(entries):
                self.rank_texts[row_index].text = f"{row_index + 1:02d}"
                self.name_texts[row_index].text = entry["name"]
                self.time_texts[row_index].text = self.store.format_time(
                    entry["time_seconds"]
                )
                self.jumps_texts[row_index].text = f"{entry['jumps']:03d}"
                self.rank_texts[row_index].draw()
                self.name_texts[row_index].draw()
                self.time_texts[row_index].draw()
                self.jumps_texts[row_index].draw()
        else:
            self.empty_text.draw()

        self.title_text.draw()
        self.subtitle_text.draw()
        self.sort_text.draw()
        self.column_rank_text.draw()
        self.column_name_text.draw()
        self.column_time_text.draw()
        self.column_jumps_text.draw()

        self._draw_button(
            self.sort_button_left,
            self.sort_button_bottom,
            self.sort_button_width,
            self.sort_button_height,
            self.sort_button_contains(self.mouse_x, self.mouse_y),
        )
        self._draw_button(
            self.back_button_left,
            self.back_button_bottom,
            self.back_button_width,
            self.back_button_height,
            self.back_contains(self.mouse_x, self.mouse_y),
        )
        self.sort_button_text.draw()
        self.back_button_text.draw()
        self.hint_text.draw()

    def _update_sort_text(self):
        """Refresh labels after changing the ranking mode."""
        if self.sort_mode == "jumps":
            self.sort_text.text = "SORTED BY FEWEST JUMPS"
            self.sort_button_text.text = "SORT: JUMPS"
        else:
            self.sort_text.text = "SORTED BY FASTEST TIME"
            self.sort_button_text.text = "SORT: TIME"

    def sort_button_contains(self, x, y):
        """Return whether a point is inside the sort button."""
        return self.sort_contains(x, y)

    @staticmethod
    def _draw_button(left, bottom, width, height, hovered):
        """Draw a compact button with a raised hover state."""
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
