"""Angled solid surfaces used by platform levels."""

import math

import arcade

from settings import PLATFORM_COLOR


class Slope:
    """A thick line segment that acts as an angled top surface."""

    def __init__(self, start_x, start_y, end_x, end_y, thickness=10):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.thickness = thickness

        self.change_x = end_x - start_x
        self.change_y = end_y - start_y
        self.length = (self.change_x**2 + self.change_y**2) ** 0.5

        if self.length == 0:
            raise ValueError("A slope must have different start and end points.")

        self.tangent_x = self.change_x / self.length
        self.tangent_y = self.change_y / self.length
        self.angle = math.atan2(self.change_y, self.change_x)

    @property
    def left(self):
        return min(self.start_x, self.end_x) - self.thickness / 2

    @property
    def right(self):
        return max(self.start_x, self.end_x) + self.thickness / 2

    @property
    def bottom(self):
        return min(self.start_y, self.end_y) - self.thickness / 2

    @property
    def top(self):
        return max(self.start_y, self.end_y) + self.thickness / 2

    def contains_x(self, x):
        """Return whether the player can stand on this slope at x."""
        return min(self.start_x, self.end_x) <= x <= max(self.start_x, self.end_x)

    def surface_y_at(self, x):
        """Return the upper edge height at a given x-coordinate."""
        progress = (x - self.start_x) / self.change_x
        center_y = self.start_y + progress * self.change_y

        # The drawn slope has thickness. Use its upper edge as the surface
        # instead of the center line so the player stands on top of it.
        upper_edge_offset = abs(self.tangent_x) * self.thickness / 2
        return center_y + upper_edge_offset

    def overlaps_rect(self, left, right, bottom, top):
        """Return whether the slope's bounds overlap another rectangle."""
        return (
            self.left < right
            and self.right > left
            and self.bottom < top
            and self.top > bottom
        )

    def draw(self):
        """Draw the slope as a thick quadrilateral."""
        normal_x = -self.tangent_y * self.thickness / 2
        normal_y = self.tangent_x * self.thickness / 2
        points = (
            self.start_x + normal_x,
            self.start_y + normal_y,
            self.end_x + normal_x,
            self.end_y + normal_y,
            self.end_x - normal_x,
            self.end_y - normal_y,
            self.start_x - normal_x,
            self.start_y - normal_y,
        )
        arcade.draw_polygon_filled(
            [(points[index], points[index + 1]) for index in range(0, len(points), 2)],
            PLATFORM_COLOR,
        )
