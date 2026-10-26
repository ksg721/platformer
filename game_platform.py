"""The stationary platform used by the game."""

import arcade

from settings import PLATFORM_COLOR


PLATFORM_BODY_COLOR = (48, 63, 83)
PLATFORM_SHADOW_COLOR = (24, 32, 49)
PLATFORM_TOP_COLOR = (112, 190, 169)
MOVING_PLATFORM_TOP_COLOR = (245, 193, 91)
PLATFORM_HIGHLIGHT_COLOR = (188, 231, 201)
PLATFORM_BOLT_COLOR = (34, 43, 61)


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
    def bottom(self):
        """Return the platform's bottom edge."""
        return self.center_y - self.height / 2

    @property
    def top(self):
        """Return the platform's top edge."""
        return self.center_y + self.height / 2

    def overlaps_rect(self, left, right, bottom, top):
        """Return whether this platform overlaps another rectangle."""
        return (
            self.left < right
            and self.right > left
            and self.bottom < top
            and self.top > bottom
        )

    def update(self, blockers=None):
        """Move without passing through walls or other platforms."""
        movement_x = 0
        movement_y = 0

        if self.movement_range_x:
            movement_x = self.speed * self.direction
            right_limit = self.start_x + self.movement_range_x
            proposed_x = self.center_x + movement_x
            if proposed_x >= right_limit:
                proposed_x = right_limit
                self.direction = -1
            elif proposed_x <= self.start_x:
                proposed_x = self.start_x
                self.direction = 1
            movement_x = proposed_x - self.center_x

        elif self.movement_range_y:
            movement_y = self.speed * self.direction
            top_limit = self.start_y + self.movement_range_y
            proposed_y = self.center_y + movement_y
            if proposed_y >= top_limit:
                proposed_y = top_limit
                self.direction = -1
            elif proposed_y <= self.start_y:
                proposed_y = self.start_y
                self.direction = 1
            movement_y = proposed_y - self.center_y

        if blockers and self._movement_is_blocked(movement_x, movement_y, blockers):
            self.direction *= -1
            reverse_x = -movement_x
            reverse_y = -movement_y
            if not self._movement_is_blocked(reverse_x, reverse_y, blockers):
                movement_x = reverse_x
                movement_y = reverse_y
            else:
                movement_x = 0
                movement_y = 0

        self.center_x += movement_x
        self.center_y += movement_y

    def _movement_is_blocked(self, movement_x, movement_y, blockers):
        """Return whether a proposed movement overlaps a blocker."""
        proposed_left = self.left + movement_x
        proposed_right = self.right + movement_x
        proposed_bottom = self.bottom + movement_y
        proposed_top = self.top + movement_y

        return any(
            blocker is not self
            and proposed_left < blocker.right
            and proposed_right > blocker.left
            and proposed_bottom < blocker.top
            and proposed_top > blocker.bottom
            for blocker in blockers
        )

    def draw(self):
        """Draw the platform with a readable, layered material style."""
        is_moving = bool(self.movement_range_x or self.movement_range_y)
        top_color = (
            MOVING_PLATFORM_TOP_COLOR
            if is_moving
            else PLATFORM_TOP_COLOR
        )

        # The offset shadow gives the thin platform a little depth.
        arcade.draw_lbwh_rectangle_filled(
            self.left + 2,
            self.bottom - 3,
            max(1, self.width - 2),
            self.height + 3,
            PLATFORM_SHADOW_COLOR,
        )
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.bottom,
            self.width,
            self.height,
            PLATFORM_BODY_COLOR,
        )
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.top - 3,
            self.width,
            3,
            top_color,
        )
        arcade.draw_line(
            self.left + 2,
            self.top - 1,
            self.right - 2,
            self.top - 1,
            PLATFORM_HIGHLIGHT_COLOR,
            1,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.left,
            self.bottom,
            self.width,
            self.height,
            PLATFORM_COLOR,
            1,
        )

        # Small bolts make moving platforms visually distinct and give the
        # wider platforms a little more texture.
        if self.width >= 24:
            for bolt_x in (self.left + 5, self.right - 5):
                arcade.draw_circle_filled(
                    bolt_x,
                    self.center_y - 1,
                    1.2,
                    PLATFORM_BOLT_COLOR,
                )

        if is_moving and self.width >= 30:
            arrow_y = self.bottom - 6
            arcade.draw_line(
                self.left + 7,
                arrow_y,
                self.right - 7,
                arrow_y,
                MOVING_PLATFORM_TOP_COLOR,
                1,
            )
