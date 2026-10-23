"""Fixed-position camera for the vertically stacked levels."""

from settings import LEVEL_HEIGHT


class Camera:
    """Keep the view locked to one level at a time."""

    def __init__(self):
        self.offset_y = 0

    def set_level(self, level_index):
        """Lock the camera to the requested level."""
        self.offset_y = level_index * LEVEL_HEIGHT

    def world_to_screen_y(self, world_y):
        """Convert a world-space y-coordinate to a screen-space coordinate."""
        return world_y - self.offset_y

    def screen_to_world_y(self, screen_y):
        """Convert a screen-space y-coordinate to a world-space coordinate."""
        return screen_y + self.offset_y
