"""Camera controls for the vertically stacked game world."""

import arcade

from settings import (
    CAMERA_SCROLL_SPEED,
    LEVEL_HEIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Camera:
    """Translate world coordinates into a locked or sliding screen view."""

    def __init__(self):
        self.offset_y = 0
        self.target_offset_y = 0
        self.transitioning = False
        self.world_camera = arcade.Camera2D()
        self.screen_camera = arcade.Camera2D()

    def set_level(self, level_index, immediate=True):
        """Point the camera at a level, optionally without animation."""
        self.target_offset_y = level_index * LEVEL_HEIGHT
        if immediate:
            self.offset_y = self.target_offset_y
            self.transitioning = False

    def start_transition(self, level_index):
        """Begin sliding the camera toward another stacked level."""
        self.target_offset_y = level_index * LEVEL_HEIGHT
        self.transitioning = True

    def update(self, delta_time):
        """Advance the camera slide and return whether it finished."""
        if not self.transitioning:
            return True

        distance = self.target_offset_y - self.offset_y
        step = CAMERA_SCROLL_SPEED * delta_time
        if abs(distance) <= step:
            self.offset_y = self.target_offset_y
            self.transitioning = False
            return True

        self.offset_y += step if distance > 0 else -step
        return False

    def use_world(self):
        """Use a camera whose origin is the current world offset."""
        self.world_camera.position = (
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + self.offset_y,
        )
        self.world_camera.use()

    def use_screen(self):
        """Use a fixed screen-space camera for HUD and background art."""
        self.screen_camera.position = (
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
        )
        self.screen_camera.use()

    def world_to_screen_y(self, world_y):
        """Convert a world-space y-coordinate to a screen-space coordinate."""
        return world_y - self.offset_y

    def screen_to_world_y(self, screen_y):
        """Convert a screen-space y-coordinate to a world-space coordinate."""
        return screen_y + self.offset_y
