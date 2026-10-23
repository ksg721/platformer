"""Main game window and coordination between game objects."""

import arcade

from level_manager import LevelManager
from levels import create_levels
from player import Player
from settings import BACKGROUND_COLOR, SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH


class PlatformerGame(arcade.Window):
    """The game window and game loop methods."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = BACKGROUND_COLOR
        self.player = Player()
        self.level_manager = LevelManager(create_levels())
        self.platforms = []

    def setup(self):
        """Create the player and the stationary platforms."""
        self.load_current_level()

    def load_current_level(self, player_x=None, spawn_from_top=False):
        """Load the platforms and starting position for the current level."""
        current_level = self.level_manager.current_level
        self.player.reset()
        self.platforms = self.level_manager.create_current_platforms()

        if spawn_from_top:
            requested_x = current_level.start_x if player_x is None else player_x
            self.player.x = max(
                self.player.width / 2,
                min(SCREEN_WIDTH - self.player.width / 2, requested_x),
            )
            self.player.y = SCREEN_HEIGHT + self.player.height / 2
            self.player.velocity_y = 0
            self.player.on_ground = False
        else:
            if player_x is None:
                self.player.x = current_level.start_x
            else:
                self.player.x = max(
                    self.player.width / 2,
                    min(SCREEN_WIDTH - self.player.width / 2, player_x),
                )
            self.player.y = current_level.start_y

        self.player.sync_world_position(current_level.world_offset_y)

    def change_level(self, direction):
        """Change levels and reload the current level when possible."""
        previous_x = self.player.x

        if direction == 1:
            level_changed = self.level_manager.next_level()
        else:
            level_changed = self.level_manager.previous_level()

        if level_changed:
            self.load_current_level(
                player_x=previous_x,
                spawn_from_top=direction == -1,
            )
        else:
            # Stay safely inside the current level at its starting position.
            self.load_current_level()

    def on_key_press(self, key, modifiers):
        """Send key-press actions to the player."""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.press_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.press_right()
        elif key in (arcade.key.W, arcade.key.SPACE, arcade.key.UP):
            self.player.press_jump(key)

    def on_key_release(self, key, modifiers):
        """Send key-release actions to the player."""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.release_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.release_right()
        elif key in (arcade.key.W, arcade.key.SPACE, arcade.key.UP):
            self.player.release_jump(key)

    def player_lands_on_platform(self, previous_bottom, platform):
        """Return whether the falling player crossed a platform's top."""
        crossed_top = previous_bottom >= platform.top and self.player.bottom <= platform.top
        overlaps_horizontally = (
            self.player.right > platform.left
            and self.player.left < platform.right
        )
        return self.player.velocity_y <= 0 and crossed_top and overlaps_horizontally

    def player_is_standing_on(self, platform):
        """Return whether the player is currently standing on a platform."""
        touching_top = abs(self.player.bottom - platform.top) < 0.1
        overlaps_horizontally = (
            self.player.right > platform.left
            and self.player.left < platform.right
        )
        return self.player.on_ground and touching_top and overlaps_horizontally

    def on_update(self, delta_time):
        """Update all game objects once per frame."""
        # Remember the platform carrying the player before platforms move.
        standing_platform = None
        for platform in self.platforms:
            if self.player_is_standing_on(platform):
                standing_platform = platform
                break

        for platform in self.platforms:
            old_x = platform.center_x
            old_y = platform.center_y
            platform.update()

            # Move the player by the same amount as the platform underneath them.
            if platform is standing_platform:
                self.player.x += platform.center_x - old_x
                self.player.y += platform.center_y - old_y

        self.player.update_jump_charge()
        self.player.update_horizontal_position()
        previous_bottom = self.player.update_vertical_position()

        for platform in self.platforms:
            if self.player_lands_on_platform(previous_bottom, platform):
                self.player.land_on(platform.top)
                break

        if self.player.top < 0:
            self.change_level(-1)

        elif self.player.bottom > SCREEN_HEIGHT:
            self.change_level(1)

        else:
            self.player.sync_world_position(self.level_manager.current_world_offset_y)

    def on_draw(self):
        """Draw all game objects."""
        self.clear()

        for platform in self.platforms:
            platform.draw()

        self.player.draw()
