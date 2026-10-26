"""Main game window and coordination between game objects."""

import arcade

from level_manager import LevelManager
from levels import create_levels
from player import Player
from settings import (
    BACKGROUND_COLOR,
    GRAVITY,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
)
from visuals import BackgroundRenderer, ParticleSystem, StructureRenderer


class PlatformerGame(arcade.Window):
    """The game window and game loop methods."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = BACKGROUND_COLOR
        self.player = Player()
        self.level_manager = LevelManager(create_levels())
        self.platforms = []
        self.walls = []
        self.slopes = []
        self.background_renderer = BackgroundRenderer()
        self.structure_renderer = StructureRenderer()
        self.particles = ParticleSystem()
        self.slide_particle_timer = 0.0
        self.title_text = arcade.Text(
            "VERTICAL ASCENT",
            26,
            SCREEN_HEIGHT - 29,
            (226, 246, 223),
            10,
            bold=True,
        )
        self.level_text = arcade.Text(
            "",
            26,
            SCREEN_HEIGHT - 43,
            (245, 197, 103),
            9,
            bold=True,
        )
        self.controls_text = arcade.Text(
            "A/D or ARROWS  MOVE     HOLD W / SPACE / UP  CHARGE",
            SCREEN_WIDTH / 2,
            16,
            (225, 236, 220, 190),
            9,
            anchor_x="center",
        )

    def setup(self):
        """Create the player and the stationary platforms."""
        self.load_current_level()

    def load_current_level(self, player_x=None, spawn_from_top=False):
        """Load the platforms and starting position for the current level."""
        current_level = self.level_manager.current_level
        self.player.reset()
        self.particles.clear()
        self.platforms = self.level_manager.create_current_platforms()
        self.slopes = self.level_manager.create_current_slopes()

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
        self.walls = self.level_manager.create_current_walls()

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
        elif key == arcade.key.N:
            self.change_level(1)
        elif key == arcade.key.P:
            self.change_level(-1)

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

    def solid_objects(self):
        """Return all objects that should block the player."""
        return self.platforms + self.walls

    def resolve_slope_collision(
        self, previous_bottom, incoming_velocity_y, previous_slope=None
    ):
        """Land on a slope when the player crosses its angled top surface."""
        for slope in self.slopes:
            slope_start = min(slope.start_x, slope.end_x)
            slope_end = max(slope.start_x, slope.end_x)
            overlaps_slope_width = (
                self.player.right > slope_start
                and self.player.left < slope_end
            )
            if not overlaps_slope_width:
                continue

            contact_x = max(slope_start, min(slope_end, self.player.x))
            surface_y = slope.surface_y_at(contact_x)
            crossed_surface = (
                incoming_velocity_y <= 0
                and previous_bottom >= surface_y - 2
                and self.player.bottom <= surface_y + 2
            )
            was_on_slope = previous_slope is slope
            is_touching_surface = self.player.bottom <= surface_y + 2
            if crossed_surface or (was_on_slope and is_touching_surface):
                self.player.land_on_slope(slope, incoming_velocity_y)
                return

        if previous_slope is not None:
            self.player.current_slope = None

    def maintain_slope_contact(self):
        """Keep the player's feet on a slope while moving across it."""
        slope = self.player.current_slope
        if slope is None or not slope.contains_x(self.player.x):
            return

        self.player.y = slope.surface_y_at(self.player.x) + self.player.height / 2
        self.player.velocity_y = 0
        self.player.on_ground = True

    def player_is_standing_on(self, platform):
        """Return whether the player is currently standing on a platform."""
        touching_top = abs(self.player.bottom - platform.top) < 0.1
        overlaps_horizontally = (
            self.player.right > platform.left
            and self.player.left < platform.right
        )
        return self.player.on_ground and touching_top and overlaps_horizontally

    def resolve_wall_collisions(self, previous_x):
        """Stop the player when horizontal movement crosses a solid object."""
        for solid_object in self.solid_objects():
            overlaps_vertically = (
                self.player.top > solid_object.bottom
                and self.player.bottom < solid_object.top
            )
            if not overlaps_vertically:
                continue

            previous_left = previous_x - self.player.width / 2
            previous_right = previous_x + self.player.width / 2

            if (
                previous_right <= solid_object.left
                and self.player.right > solid_object.left
            ):
                self.player.x = solid_object.left - self.player.width / 2
                self.player.velocity_x = 0
            elif (
                previous_left >= solid_object.right
                and self.player.left < solid_object.right
            ):
                self.player.x = solid_object.right + self.player.width / 2
                self.player.velocity_x = 0

    def resolve_vertical_collisions(self, previous_bottom, previous_top):
        """Land on or bounce off the top and bottom of solid objects."""
        for solid_object in self.solid_objects():
            overlaps_horizontally = (
                self.player.right > solid_object.left
                and self.player.left < solid_object.right
            )
            if not overlaps_horizontally:
                continue

            if (
                self.player.velocity_y <= 0
                and previous_bottom >= solid_object.top
                and self.player.bottom < solid_object.top
            ):
                self.player.land_on(solid_object.top)
                return

            if (
                self.player.velocity_y > 0
                and previous_top <= solid_object.bottom
                and self.player.top > solid_object.bottom
            ):
                self.player.y = solid_object.bottom - self.player.height / 2
                self.player.velocity_y = 0
                return

    def resolve_carried_vertical_collisions(self, previous_y, standing_platform):
        """Stop a moving platform from carrying the player through solids."""
        vertical_change = self.player.y - previous_y
        if abs(vertical_change) < 0.001:
            return

        previous_bottom = previous_y - self.player.height / 2
        previous_top = previous_y + self.player.height / 2

        for solid_object in self.solid_objects():
            if solid_object is standing_platform:
                continue

            overlaps_horizontally = (
                self.player.right > solid_object.left
                and self.player.left < solid_object.right
            )
            overlaps_vertically = (
                self.player.top > solid_object.bottom
                and self.player.bottom < solid_object.top
            )
            if not overlaps_horizontally or not overlaps_vertically:
                continue

            if vertical_change > 0 and previous_top <= solid_object.bottom:
                self.player.y = solid_object.bottom - self.player.height / 2
                self.player.velocity_y = 0
                return

            if vertical_change < 0 and previous_bottom >= solid_object.top:
                self.player.land_on(solid_object.top)
                return

    def on_update(self, delta_time):
        """Update all game objects once per frame."""
        self.background_renderer.update(delta_time)
        self.particles.update(delta_time)
        self.slide_particle_timer -= delta_time

        was_on_ground = self.player.on_ground

        # Remember the platform carrying the player before platforms move.
        standing_platform = None
        for platform in self.platforms:
            if self.player_is_standing_on(platform):
                standing_platform = platform
                break

        previous_carried_x = self.player.x
        previous_carried_y = self.player.y

        for platform in self.platforms:
            old_x = platform.center_x
            old_y = platform.center_y
            blockers = self.walls + self.slopes + [
                other for other in self.platforms if other is not platform
            ]
            platform.update(blockers)

            # Move the player by the same amount as the platform underneath them.
            if platform is standing_platform:
                self.player.x += platform.center_x - old_x
                self.player.y += platform.center_y - old_y

        # A moving platform can carry the player into a wall even when the
        # player is not pressing a movement key. Resolve that carry movement
        # before applying the player's own movement for this frame.
        if standing_platform is not None:
            self.resolve_wall_collisions(previous_carried_x)
            self.resolve_carried_vertical_collisions(
                previous_carried_y,
                standing_platform,
            )

        self.player.update_jump_charge()
        if (
            self.player.current_slope
            and self.player.on_ground
        ):
            self.player.update_slope_physics(self.player.current_slope)

        previous_x = self.player.x
        self.player.update_horizontal_position()
        self.resolve_wall_collisions(previous_x)
        self.maintain_slope_contact()
        previous_top = self.player.top
        incoming_velocity_y = self.player.velocity_y
        previous_slope = self.player.current_slope
        previous_bottom = self.player.update_vertical_position()
        self.resolve_vertical_collisions(previous_bottom, previous_top)
        if not self.player.on_ground:
            self.resolve_slope_collision(
                previous_bottom,
                incoming_velocity_y,
                previous_slope,
            )

        # Visual feedback is based on the same physics transitions that the
        # player experiences, so effects never change gameplay behavior.
        if was_on_ground and not self.player.on_ground and self.player.velocity_y > 0:
            self.particles.emit_jump(self.player.x, self.player.bottom)
        elif not was_on_ground and self.player.on_ground:
            self.particles.emit_landing(
                self.player.x,
                self.player.bottom,
                incoming_velocity_y,
            )

        if self.player.slope_sliding and self.slide_particle_timer <= 0:
            direction = 1 if self.player.velocity_x >= 0 else -1
            self.particles.emit_slide(
                self.player.x,
                self.player.bottom,
                direction,
            )
            self.slide_particle_timer = 0.1

        if self.player.top < 0:
            self.change_level(-1)

        elif self.player.bottom > SCREEN_HEIGHT:
            self.change_level(1)

        else:
            self.player.sync_world_position(self.level_manager.current_world_offset_y)

    def on_draw(self):
        """Draw all game objects."""
        self.clear()

        self.background_renderer.draw(self.level_manager.current_level_number)
        self.structure_renderer.draw(self.level_manager.current_level_number)

        for wall in self.walls:
            wall.draw()

        for slope in self.slopes:
            slope.draw()

        for platform in self.platforms:
            platform.draw()

        self.particles.draw()
        self.player.draw()
        self.draw_hud()

    def draw_hud(self):
        """Draw compact interface information above the game world."""
        level_number = self.level_manager.current_level_number
        total_levels = self.level_manager.total_levels

        arcade.draw_lbwh_rectangle_filled(
            16,
            SCREEN_HEIGHT - 48,
            180,
            32,
            (14, 22, 40, 190),
        )
        arcade.draw_lbwh_rectangle_outline(
            16,
            SCREEN_HEIGHT - 48,
            180,
            32,
            (143, 211, 191),
            1,
        )
        self.level_text.text = f"LEVEL {level_number:02d} / {total_levels:02d}"
        self.title_text.draw()
        self.level_text.draw()

        progress_left = SCREEN_WIDTH - 170
        progress_bottom = SCREEN_HEIGHT - 38
        progress_width = 138
        arcade.draw_lbwh_rectangle_filled(
            progress_left,
            progress_bottom,
            progress_width,
            5,
            (14, 22, 40, 190),
        )
        progress_ratio = (level_number - 1) / max(1, total_levels - 1)
        arcade.draw_lbwh_rectangle_filled(
            progress_left,
            progress_bottom,
            progress_width * progress_ratio,
            5,
            (143, 211, 191),
        )
        self.controls_text.draw()
