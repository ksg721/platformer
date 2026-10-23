"""Vertical wall obstacles used by platform levels."""

import arcade

from settings import WALL_COLOR


class Wall:
    """A stationary rectangular wall that blocks horizontal movement."""

    def __init__(self, center_x, center_y, width, height):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.center_x - self.width / 2

    @property
    def right(self):
        return self.center_x + self.width / 2

    @property
    def bottom(self):
        return self.center_y - self.height / 2

    @property
    def top(self):
        return self.center_y + self.height / 2

    def draw(self):
        """Draw the wall."""
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.bottom,
            self.width,
            self.height,
            WALL_COLOR,
        )
