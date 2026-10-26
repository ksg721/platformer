"""Vertical wall obstacles used by platform levels."""

import arcade

from settings import LEVEL_HEIGHT, WALL_COLOR


WALL_BODY_COLOR = (44, 49, 70)
WALL_SHADOW_COLOR = (24, 28, 46)
WALL_HIGHLIGHT_COLOR = (102, 121, 153)
WALL_SEAM_COLOR = (30, 34, 52)
WALL_BOLT_COLOR = (227, 179, 91)
WALL_CAP_COLOR = (77, 103, 125)


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
        """Draw a reinforced buttress instead of a plain rectangle."""
        arcade.draw_lbwh_rectangle_filled(
            self.left + 3,
            self.bottom - 2,
            self.width,
            self.height + 2,
            WALL_SHADOW_COLOR,
        )
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.bottom,
            self.width,
            self.height,
            WALL_BODY_COLOR,
        )
        body_points = [
            (self.left, self.bottom + 5),
            (self.left + 3, self.bottom),
            (self.right - 3, self.bottom),
            (self.right, self.bottom + 5),
            (self.right, self.top - 5),
            (self.right - 3, self.top),
            (self.left + 3, self.top),
            (self.left, self.top - 5),
        ]
        arcade.draw_polygon_filled(body_points, WALL_BODY_COLOR)
        arcade.draw_polygon_outline(body_points, WALL_COLOR, 1)

        # Wide anchor caps make each obstacle read as a load-bearing part of
        # the tower instead of a narrow free-standing platform.
        cap_half_width = self.width / 2 + 5
        cap_height = min(6, self.height / 4)
        for cap_y in (self.bottom, self.top - cap_height):
            cap_points = [
                (self.center_x - cap_half_width, cap_y),
                (self.center_x + cap_half_width, cap_y),
                (self.center_x + cap_half_width - 4, cap_y + cap_height),
                (self.center_x - cap_half_width + 4, cap_y + cap_height),
            ]
            arcade.draw_polygon_filled(cap_points, WALL_CAP_COLOR)
            arcade.draw_polygon_outline(cap_points, WALL_HIGHLIGHT_COLOR, 1)

        # Use a vertical channel for wall spines and a horizontal channel
        # for cross-braces, so both pieces read as the same material.
        is_horizontal = self.width >= self.height * 1.8
        if is_horizontal:
            channel_height = max(3, self.height * 0.28)
            arcade.draw_lbwh_rectangle_filled(
                self.left + 4,
                self.center_y - channel_height / 2,
                max(1, self.width - 8),
                channel_height,
                WALL_SHADOW_COLOR,
            )
            arcade.draw_line(
                self.left + 5,
                self.center_y,
                self.right - 5,
                self.center_y,
                WALL_HIGHLIGHT_COLOR,
                1,
            )
            seam_x = self.left + self.width * 0.5
            arcade.draw_line(
                seam_x,
                self.bottom + 3,
                seam_x,
                self.top - 2,
                WALL_SEAM_COLOR,
                1,
            )
        else:
            channel_width = max(3, self.width * 0.28)
            arcade.draw_lbwh_rectangle_filled(
                self.center_x - channel_width / 2,
                self.bottom + 4,
                channel_width,
                max(1, self.height - 8),
                WALL_SHADOW_COLOR,
            )
            arcade.draw_line(
                self.center_x,
                self.bottom + 5,
                self.center_x,
                self.top - 5,
                WALL_HIGHLIGHT_COLOR,
                1,
            )

            seam_y = self.bottom + self.height * 0.5
            arcade.draw_line(
                self.left + 3,
                seam_y,
                self.right - 2,
                seam_y,
                WALL_SEAM_COLOR,
                1,
            )
        for bolt_y in (self.bottom + 5, self.top - 5):
            if self.height >= 18:
                arcade.draw_circle_filled(
                    self.left + 4,
                    bolt_y,
                    1.4,
                    WALL_BOLT_COLOR,
                )
                arcade.draw_circle_filled(
                    self.right - 4,
                    bolt_y,
                    1.4,
                    WALL_BOLT_COLOR,
                )

        # Long barrier sections are divided into repeating construction
        # plates so they read as one engineered wall, not a tall rectangle.
        section_count = int(self.height // 55)
        for section in range(1, section_count + 1):
            seam_y = self.bottom + section * 55
            if seam_y < self.top - 8:
                arcade.draw_line(
                    self.left + 3,
                    seam_y,
                    self.right - 3,
                    seam_y,
                    WALL_SEAM_COLOR,
                    1,
                )


class WallBarrier:
    """Create a continuous vertical wall with intentional openings.

    A barrier is authored once per level as a center x-position and a list of
    open vertical ranges. Everything outside those openings becomes a solid
    wall segment. Related positions, offsets, widths, and cross-braces let the
    tower spine drift organically from level to level while remaining one
    connected architectural system.
    """

    def __init__(
        self,
        center_x,
        width,
        openings,
        height=LEVEL_HEIGHT,
        segment_offsets=None,
        segment_widths=None,
        cross_braces=None,
    ):
        self.center_x = center_x
        self.width = width
        self.height = height
        self.segment_offsets = segment_offsets or []
        self.segment_widths = segment_widths or []
        self.cross_braces = cross_braces or []
        self.openings = self.normalize_openings(openings)

    def normalize_openings(self, openings):
        """Clamp, sort, and merge openings before creating wall segments."""
        clean_openings = []
        for opening_bottom, opening_top in openings:
            opening_bottom = max(0, min(self.height, opening_bottom))
            opening_top = max(0, min(self.height, opening_top))
            if opening_top <= opening_bottom:
                continue
            clean_openings.append((opening_bottom, opening_top))

        clean_openings.sort()
        merged = []
        for opening in clean_openings:
            if merged and opening[0] <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], opening[1]))
            else:
                merged.append(opening)
        return merged

    def create_walls(self, world_offset_y=0):
        """Return solid wall segments for the spaces outside the openings."""
        walls = []
        cursor = 0

        def append_segment(bottom, top):
            """Create one organically offset segment."""
            segment_index = len(walls)
            offset = (
                self.segment_offsets[segment_index]
                if segment_index < len(self.segment_offsets)
                else 0
            )
            width = (
                self.segment_widths[segment_index]
                if segment_index < len(self.segment_widths)
                else self.width
            )
            walls.append(
                Wall(
                    self.center_x + offset,
                    world_offset_y + (bottom + top) / 2,
                    width,
                    top - bottom,
                )
            )

        for opening_bottom, opening_top in self.openings:
            if opening_bottom > cursor:
                append_segment(cursor, opening_bottom)
            cursor = max(cursor, opening_top)

        if cursor < self.height:
            append_segment(cursor, self.height)

        # Cross-braces are authored as part of the same barrier so they can
        # tie a spine into the surrounding tower without a second wall system.
        for brace_data in self.cross_braces:
            brace = brace_data.copy()
            brace["center_y"] += world_offset_y
            walls.append(Wall(**brace))

        return walls
