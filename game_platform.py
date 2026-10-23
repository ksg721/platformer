"""The stationary platform used by the game."""

import arcade

from settings import PLATFORM_COLOR


class Platform:
    """A rectangular platform that can be stationary or moving."""

    def __init__(
        self,
        center_x,
        center_y,
        width,
        height,
        movement_range_x=0,
        movement_range_y=0,
        speed=0,
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

        self.start_x = center_x
        self.start_y = center_y
        self.movement_range_x = movement_range_x
        self.movement_range_y = movement_range_y
        self.speed = speed
        self.direction = 1

    @property
    def left(self):
        """Return the platform's left edge."""
        return self.center_x - self.width / 2

    @property
    def right(self):
        """Return the platform's right edge."""
        return self.center_x + self.width / 2

    @property
    def top(self):
        """Return the platform's top edge."""
        return self.center_y + self.height / 2

    def update(self):
        """Move the platform back and forth within its movement range."""
        if self.movement_range_x:
            self.center_x += self.speed * self.direction
            right_limit = self.start_x + self.movement_range_x

            if self.center_x >= right_limit:
                self.center_x = right_limit
                self.direction = -1
            elif self.center_x <= self.start_x:
                self.center_x = self.start_x
                self.direction = 1

        if self.movement_range_y:
            self.center_y += self.speed * self.direction
            top_limit = self.start_y + self.movement_range_y

            if self.center_y >= top_limit:
                self.center_y = top_limit
                self.direction = -1
            elif self.center_y <= self.start_y:
                self.center_y = self.start_y
                self.direction = 1

    def draw(self):
        """Draw the platform."""
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.center_y - self.height / 2,
            self.width,
            self.height,
            PLATFORM_COLOR,
        )
