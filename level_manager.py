"""Level navigation and level loading."""

from level import Level


class LevelManager:
    """Keep track of the current level and navigate between levels."""

    def __init__(self, levels):
        """Create a manager using a non-empty list of Level objects."""
        if not levels:
            raise ValueError("LevelManager requires at least one level.")

        if not all(isinstance(level, Level) for level in levels):
            raise TypeError("All items must be Level objects.")

        self.levels = levels
        self.current_index = 0

    @property
    def current_level(self):
        """Return the currently selected Level object."""
        return self.levels[self.current_index]

    @property
    def current_level_number(self):
        """Return the current level number using normal counting from 1."""
        return self.current_index + 1

    @property
    def total_levels(self):
        """Return the total number of available levels."""
        return len(self.levels)

    @property
    def current_world_offset_y(self):
        """Return the current level's vertical world offset."""
        return self.current_level.world_offset_y

    def create_current_platforms(self, world_coordinates=False):
        """Create platforms for the current level."""
        return self.current_level.create_platforms(world_coordinates)

    def create_current_walls(self, world_coordinates=False):
        """Create walls for the current level."""
        return self.current_level.create_walls(world_coordinates)

    def create_current_slopes(self, world_coordinates=False):
        """Create angled surfaces for the current level."""
        return self.current_level.create_slopes(world_coordinates)

    def next_level(self):
        """Move to the next level if one exists.

        Return True when the level changed and False at the final level.
        """
        if self.current_index >= self.total_levels - 1:
            return False

        self.current_index += 1
        return True

    def previous_level(self):
        """Move to the previous level if one exists.

        Return True when the level changed and False at level 1.
        """
        if self.current_index <= 0:
            return False

        self.current_index -= 1
        return True
