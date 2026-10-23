"""Level data and platform creation."""

from game_platform import Platform
from settings import LEVEL_HEIGHT
from slope import Slope
from wall import Wall


class Level:
    """Store the layout and starting information for one game level."""

    def __init__(
        self,
        platform_data,
        start_x,
        start_y,
        level_index=0,
        wall_data=None,
        slope_data=None,
    ):
        """Create a level from platform settings.

        Each platform entry is a dictionary containing the arguments needed
        to create a Platform object. Optional movement settings can be
        included for moving platforms.
        """
        self.platform_data = platform_data
        self.start_x = start_x
        self.start_y = start_y
        self.level_index = level_index
        self.wall_data = wall_data or []
        self.slope_data = slope_data or []

    @property
    def world_offset_y(self):
        """Return this level's vertical position in the world."""
        return self.level_index * LEVEL_HEIGHT

    def create_platforms(self, world_coordinates=False):
        """Create and return this level's platforms.

        By default, platforms use coordinates local to the level. When
        world_coordinates is True, their vertical positions include the
        level's world offset.
        """
        platforms = []
        for data in self.platform_data:
            platform_data = data.copy()
            if world_coordinates:
                platform_data["center_y"] += self.world_offset_y
            platforms.append(Platform(**platform_data))
        return platforms

    def create_walls(self, world_coordinates=False):
        """Create and return this level's walls."""
        walls = []
        for data in self.wall_data:
            wall_data = data.copy()
            if world_coordinates:
                wall_data["center_y"] += self.world_offset_y
            walls.append(Wall(**wall_data))
        return walls

    def create_slopes(self, world_coordinates=False):
        """Create and return this level's angled surfaces."""
        slopes = []
        for data in self.slope_data:
            slope_data = data.copy()
            if world_coordinates:
                slope_data["start_y"] += self.world_offset_y
                slope_data["end_y"] += self.world_offset_y
            slopes.append(Slope(**slope_data))
        return slopes
