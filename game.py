"""Main game window and coordination between game objects."""

import arcade

from camera import Camera
from leaderboard import LeaderboardStore
from leaderboard_screen import LeaderboardScreen
from level_manager import LevelManager
from levels import create_levels
from pause_screen import PauseScreen
from player import Player
from start_screen import StartScreen
from settings import (
    BACKGROUND_COLOR,
    GRAVITY,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    WALL_BOUNCE_FACTOR,
)
from settings_screen import SettingsScreen
from user_settings import SettingsStore
from visuals import BackgroundRenderer, ParticleSystem, StructureRenderer
from wall import Wall
from win_screen import WinScreen


class PlatformerGame(arcade.Window):
    """The game window and game loop methods."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = BACKGROUND_COLOR
        self.player = Player()
        self.camera = Camera()
        self.level_manager = LevelManager(create_levels())
        self.platforms = []
        self.walls = []
        self.boundary_walls = []
        self.slopes = []
        self.previous_platforms = []
        self.previous_walls = []
        self.previous_slopes = []
        self.background_renderer = BackgroundRenderer()
        self.structure_renderer = StructureRenderer()
        self.particles = ParticleSystem()
        self.slide_particle_timer = 0.0
        self.ignore_next_mouse_release = False
        self.elapsed_time = 0.0
        self.jump_count = 0
        self.settings_store = SettingsStore()
        self.leaderboard_store = LeaderboardStore()
        self.start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.win_screen = WinScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.leaderboard_screen = LeaderboardScreen(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.leaderboard_store,
        )
        self.settings_screen = SettingsScreen(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.settings_store,
        )
        self.pause_screen = PauseScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.settings_return_to_pause = False
        self.leaderboard_return_to_win = False
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
        self.stats_text = arcade.Text(
            "",
            220,
            SCREEN_HEIGHT - 29,
            (226, 246, 223),
            9,
            bold=True,
        )
        self.controls_text = arcade.Text(
            "A/D or ARROWS  MOVE     HOLD LEFT CLICK  AIM + CHARGE",
            SCREEN_WIDTH / 2,
            16,
            (225, 236, 220, 190),
            9,
            anchor_x="center",
        )
        self.apply_settings()

    def setup(self):
        """Create the player and the stationary platforms."""
        self.load_current_level()

    def on_resize(self, width, height):
        """Keep the virtual 800x600 game centered after window resizing."""
        if hasattr(self, "camera"):
            self.camera.resize(width, height)

    def load_level_objects(self):
        """Load the current level's objects in world coordinates."""
        self.platforms = self.level_manager.create_current_platforms(
            world_coordinates=True
        )
        self.walls = self.level_manager.create_current_walls(
            world_coordinates=True
        )
        self.slopes = self.level_manager.create_current_slopes(
            world_coordinates=True
        )
        self.boundary_walls = self.create_boundary_walls()

    def create_boundary_walls(self):
        """Create collision-only walls matching the visible side buttresses."""
        level = self.level_manager.current_level
        world_bottom = level.world_offset_y
        wall_width = 67
        wall_height = SCREEN_HEIGHT
        return [
            Wall(
                wall_width / 2,
                world_bottom + wall_height / 2,
                wall_width,
                wall_height,
            ),
            Wall(
                SCREEN_WIDTH - wall_width / 2,
                world_bottom + wall_height / 2,
                wall_width,
                wall_height,
            ),
        ]

    def load_current_level(self, player_x=None, spawn_from_top=False):
        """Load the platforms and starting position for the current level."""
        current_level = self.level_manager.current_level
        self.camera.set_level(current_level.level_index)
        self.player.reset()
        self.particles.clear()
        self.previous_platforms = []
        self.previous_walls = []
        self.previous_slopes = []
        self.load_level_objects()

        if spawn_from_top:
            requested_x = current_level.start_x if player_x is None else player_x
            self.player.x = max(
                self.player.width / 2,
                min(SCREEN_WIDTH - self.player.width / 2, requested_x),
            )
            self.player.y = (
                current_level.world_offset_y
                + SCREEN_HEIGHT
                + self.player.height / 2
            )
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
            self.player.y = current_level.world_offset_y + current_level.start_y

        self.player.set_camera_offset(self.camera.offset_y)
        self.player.sync_world_position()

    def restart_game(self):
        """Return the player to Level 1 after completing the climb."""
        self.level_manager.current_index = 0
        self.elapsed_time = 0.0
        self.jump_count = 0
        self.start_screen.show()
        self.win_screen.hide()
        self.leaderboard_screen.hide()
        self.settings_screen.hide()
        self.pause_screen.hide()
        self.settings_return_to_pause = False
        self.leaderboard_return_to_win = False
        self.load_current_level()

    def start_game(self):
        """Hide the title screen and begin the timed climb."""
        self.start_screen.hide()
        self.leaderboard_screen.hide()
        self.settings_screen.hide()
        self.pause_screen.hide()
        self.settings_return_to_pause = False
        self.elapsed_time = 0.0
        self.jump_count = 0

    def open_settings(self, return_to_pause=False):
        """Open the settings menu from the title or pause screen."""
        self.settings_return_to_pause = return_to_pause
        self.start_screen.hide()
        self.pause_screen.hide()
        self.settings_screen.show()

    def close_settings(self):
        """Return from settings to the screen that opened it."""
        self.settings_screen.hide()
        if self.settings_return_to_pause:
            self.pause_screen.show()
        else:
            self.start_screen.show()
        self.settings_return_to_pause = False
        self.apply_settings()

    def pause_game(self):
        """Pause the active climb and release held movement inputs."""
        if self.pause_screen.visible:
            return

        self.player.left_pressed = False
        self.player.right_pressed = False
        self.player.jump_keys_held.clear()
        self.player.jump_charge = 0
        self.pause_screen.show()

    def resume_game(self):
        """Hide the pause menu and resume the active climb."""
        self.pause_screen.hide()

    def restart_from_pause(self):
        """Restart the run immediately from the pause menu."""
        self.restart_game()
        self.start_screen.hide()

    def exit_to_title(self):
        """Reset the current run and return to the title screen."""
        self.restart_game()

    def apply_settings(self, apply_display=True):
        """Apply saved preferences to the window and gameplay objects."""
        self.player.set_aim_settings(
            self.settings_store.get("mouse_sensitivity"),
            self.settings_store.get("invert_mouse"),
        )
        self.player.show_power_bar = self.settings_store.get("show_power_bar")
        self.particles.enabled = not self.settings_store.get("reduced_effects")
        if not self.particles.enabled:
            self.particles.clear()
        self.camera.reduced_motion = self.settings_store.get(
            "reduced_camera_motion"
        )

        if apply_display:
            desired_fullscreen = self.settings_store.get("fullscreen")
            if self.fullscreen != desired_fullscreen:
                self.set_fullscreen(desired_fullscreen)
        self.camera.resize(self.width, self.height)

    def activate_setting(self, row_index):
        """Change one setting from the settings menu and apply it."""
        self.settings_screen.activate_row(row_index)
        setting_key = self.settings_screen.ROWS[row_index][0]
        self.apply_settings(apply_display=setting_key != "fullscreen")
        if setting_key == "fullscreen":
            self.settings_screen.message = "DISPLAY MODE WILL APPLY WHEN YOU EXIT"

    def reset_default_settings(self):
        """Restore defaults and apply them immediately."""
        self.settings_screen.reset_defaults()
        self.apply_settings(apply_display=False)
        self.settings_screen.message = "DEFAULTS SAVED  •  DISPLAY APPLIES ON EXIT"

    def reset_leaderboard(self):
        """Clear saved scores after the settings menu confirms the action."""
        if not self.settings_screen.request_leaderboard_reset():
            return

        if self.leaderboard_store.clear():
            self.settings_screen.message = "LEADERBOARD CLEARED"
        else:
            self.settings_screen.message = "COULD NOT CLEAR LEADERBOARD"

    def open_leaderboard(self, return_to_win=False):
        """Show the leaderboard from either the title or win screen."""
        self.leaderboard_return_to_win = return_to_win
        if not return_to_win:
            self.start_screen.hide()
            self.win_screen.hide()
        self.leaderboard_screen.show()

    def close_leaderboard(self):
        """Return to the screen that opened the leaderboard."""
        self.leaderboard_screen.hide()
        if self.leaderboard_return_to_win:
            self.win_screen.visible = True
        else:
            self.start_screen.show()
        self.leaderboard_return_to_win = False

    def save_score(self):
        """Save the completed run after the player provides a name."""
        if not self.win_screen.visible or self.win_screen.score_saved:
            return

        if not self.win_screen.name_input.strip():
            self.win_screen.show_save_error()
            return

        saved_entry = self.leaderboard_store.add_score(
            self.win_screen.name_input,
            self.elapsed_time,
            self.jump_count,
        )
        if saved_entry is None:
            self.win_screen.show_save_failure()
        else:
            self.win_screen.mark_saved()

    def formatted_elapsed_time(self):
        """Return the run time as minutes and seconds."""
        total_seconds = max(0, int(self.elapsed_time))
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def check_win_condition(self):
        """Show the win screen when the player reaches Level 10's last platform."""
        if self.win_screen.visible:
            return

        if self.level_manager.current_level_number != self.level_manager.total_levels:
            return

        if not self.platforms:
            return

        final_platform = self.platforms[-1]
        if self.player_is_standing_on(final_platform):
            self.player.left_pressed = False
            self.player.right_pressed = False
            self.player.jump_keys_held.clear()
            self.player.jump_charge = 0
            self.player.velocity_x = 0
            self.player.velocity_y = 0
            self.particles.clear()
            self.win_screen.show(self.elapsed_time, self.jump_count)

    def change_level(self, direction):
        """Change levels and reload the current level when possible."""
        if self.camera.transitioning:
            return

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

    def transition_to_adjacent_level(self, direction):
        """Move into the neighboring screen without resetting the player."""
        if self.camera.transitioning:
            return

        old_platforms = self.platforms
        old_walls = self.walls
        old_slopes = self.slopes

        if direction == 1:
            level_changed = self.level_manager.next_level()
        else:
            level_changed = self.level_manager.previous_level()

        if not level_changed:
            current_level = self.level_manager.current_level
            if direction == 1:
                self.player.y = (
                    current_level.world_offset_y
                    + SCREEN_HEIGHT
                    - self.player.height / 2
                )
            else:
                # Level 1 has no lower screen to receive the fall. Return to
                # its actual starting platform instead of preserving an x
                # position that may be outside the platform's bounds.
                self.player.x = current_level.start_x
                self.player.y = (
                    current_level.world_offset_y
                    + current_level.start_y
                )
            self.player.velocity_y = 0
            self.player.on_ground = True
            return

        self.previous_platforms = old_platforms
        self.previous_walls = old_walls
        self.previous_slopes = old_slopes
        self.load_level_objects()
        self.particles.clear()

        if direction == 1 and self.platforms:
            # The first platform is the shared arrival landing between
            # screens. Place the player on its top during the camera slide so
            # full collision does not trap them against its underside.
            arrival_platform = self.platforms[0]
            overlaps_arrival = (
                self.player.right > arrival_platform.left
                and self.player.left < arrival_platform.right
            )
            if overlaps_arrival:
                self.player.land_on(arrival_platform.top)

        self.camera.start_transition(
            self.level_manager.current_level.level_index
        )
        self.player.set_camera_offset(self.camera.offset_y)

    def update_camera_transition(self, delta_time):
        """Advance a screen slide and clear the old screen when complete."""
        finished = self.camera.update(delta_time)
        self.player.set_camera_offset(self.camera.offset_y)
        if finished:
            self.previous_platforms = []
            self.previous_walls = []
            self.previous_slopes = []
        return finished

    def on_key_press(self, key, modifiers):
        """Send key-press actions to the player."""
        if self.settings_screen.visible:
            if key in (arcade.key.ESCAPE, arcade.key.B):
                self.close_settings()
            return

        if self.leaderboard_screen.visible:
            if key in (arcade.key.ESCAPE, arcade.key.B):
                self.close_leaderboard()
            elif key == arcade.key.T:
                self.leaderboard_screen.toggle_sort()
            return

        if self.win_screen.visible:
            if key == arcade.key.R:
                self.restart_game()
            elif key == arcade.key.BACKSPACE:
                self.win_screen.handle_backspace()
            elif key == arcade.key.ENTER:
                self.save_score()
            elif key == arcade.key.L and self.win_screen.score_saved:
                self.open_leaderboard(return_to_win=True)
            return

        if self.pause_screen.visible:
            if key in (arcade.key.ESCAPE, arcade.key.B):
                self.resume_game()
            elif key == arcade.key.R:
                self.restart_from_pause()
            elif key == arcade.key.S:
                self.open_settings(return_to_pause=True)
            return

        if self.start_screen.visible:
            if key in (arcade.key.ENTER, arcade.key.SPACE):
                self.start_game()
            elif key == arcade.key.L:
                self.open_leaderboard()
            elif key == arcade.key.S:
                self.open_settings()
            return

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.press_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.press_right()
        elif key == arcade.key.ESCAPE:
            self.pause_game()
        elif key == arcade.key.N:
            self.change_level(1)
        elif key == arcade.key.P:
            self.change_level(-1)

    def on_key_release(self, key, modifiers):
        """Send key-release actions to the player."""
        if (
            self.win_screen.visible
            or self.start_screen.visible
            or self.leaderboard_screen.visible
            or self.settings_screen.visible
            or self.pause_screen.visible
        ):
            return

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.release_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.release_right()

    def on_mouse_motion(self, x, y, dx, dy):
        """Update the player's jump aim as the mouse moves."""
        virtual_x, virtual_y, inside_viewport = self.camera.window_to_virtual(x, y)
        if not inside_viewport:
            virtual_x = -100
            virtual_y = -100
        if self.settings_screen.visible:
            self.settings_screen.set_mouse_position(virtual_x, virtual_y)
            return
        if self.leaderboard_screen.visible:
            self.leaderboard_screen.set_mouse_position(virtual_x, virtual_y)
            return
        if self.win_screen.visible:
            self.win_screen.set_mouse_position(virtual_x, virtual_y)
            return
        if self.pause_screen.visible:
            self.pause_screen.set_mouse_position(virtual_x, virtual_y)
            return
        if self.start_screen.visible:
            self.start_screen.set_mouse_position(virtual_x, virtual_y)
            return
        if inside_viewport:
            self.player.set_mouse_position(virtual_x, virtual_y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Start charging a jump with the left mouse button."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            virtual_x, virtual_y, inside_viewport = self.camera.window_to_virtual(x, y)
            if not inside_viewport:
                return
            if self.settings_screen.visible:
                if self.settings_screen.back_button_contains(virtual_x, virtual_y):
                    self.close_settings()
                elif self.settings_screen.reset_leaderboard_button_contains(
                    virtual_x,
                    virtual_y,
                ):
                    self.reset_leaderboard()
                elif self.settings_screen.reset_defaults_button_contains(
                    virtual_x,
                    virtual_y,
                ):
                    self.reset_default_settings()
                else:
                    row_index = self.settings_screen.row_at(virtual_x, virtual_y)
                    if row_index is not None:
                        self.activate_setting(row_index)
                self.ignore_next_mouse_release = True
                return
            if self.leaderboard_screen.visible:
                if self.leaderboard_screen.back_contains(virtual_x, virtual_y):
                    self.close_leaderboard()
                    self.ignore_next_mouse_release = True
                elif self.leaderboard_screen.sort_contains(virtual_x, virtual_y):
                    self.leaderboard_screen.toggle_sort()
                    self.ignore_next_mouse_release = True
                return
            if self.win_screen.visible:
                if self.win_screen.save_button_contains(virtual_x, virtual_y):
                    if self.win_screen.score_saved:
                        self.open_leaderboard(return_to_win=True)
                    else:
                        self.save_score()
                    self.ignore_next_mouse_release = True
                return
            if self.pause_screen.visible:
                if self.pause_screen.restart_button_contains(virtual_x, virtual_y):
                    self.restart_from_pause()
                    self.ignore_next_mouse_release = True
                elif self.pause_screen.settings_button_contains(
                    virtual_x,
                    virtual_y,
                ):
                    self.open_settings(return_to_pause=True)
                    self.ignore_next_mouse_release = True
                elif self.pause_screen.title_button_contains(virtual_x, virtual_y):
                    self.exit_to_title()
                    self.ignore_next_mouse_release = True
                return
            if self.start_screen.visible:
                if self.start_screen.button_contains(virtual_x, virtual_y):
                    self.start_game()
                    self.ignore_next_mouse_release = True
                elif self.start_screen.leaderboard_button_contains(
                    virtual_x,
                    virtual_y,
                ):
                    self.open_leaderboard()
                    self.ignore_next_mouse_release = True
                elif self.start_screen.settings_button_contains(virtual_x, virtual_y):
                    self.open_settings()
                    self.ignore_next_mouse_release = True
                elif self.start_screen.quit_button_contains(virtual_x, virtual_y):
                    self.close()
                    self.ignore_next_mouse_release = True
                return
            self.player.set_mouse_position(virtual_x, virtual_y)
            self.player.press_jump(button)

    def on_text(self, text):
        """Forward typed characters to the completion name field."""
        if self.win_screen.visible and not self.leaderboard_screen.visible:
            self.win_screen.handle_text(text)

    def on_mouse_release(self, x, y, button, modifiers):
        """Launch the charged jump when the left mouse button is released."""
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.ignore_next_mouse_release:
            self.ignore_next_mouse_release = False
            return

        virtual_x, virtual_y, inside_viewport = self.camera.window_to_virtual(x, y)
        if not inside_viewport:
            virtual_x = self.player.mouse_x
            virtual_y = self.player.mouse_y

        if (
            not self.win_screen.visible
            and not self.start_screen.visible
            and not self.leaderboard_screen.visible
            and not self.settings_screen.visible
            and not self.pause_screen.visible
        ):
            jump_started = self.player.release_jump(button, virtual_x, virtual_y)
            if jump_started:
                self.jump_count += 1

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
        return self.platforms + self.walls + self.boundary_walls

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
                incoming_speed = max(
                    abs(self.player.velocity_x),
                    abs(self.player.x - previous_x),
                )
                self.player.velocity_x = -incoming_speed * WALL_BOUNCE_FACTOR
            elif (
                previous_left >= solid_object.right
                and self.player.left < solid_object.right
            ):
                self.player.x = solid_object.right + self.player.width / 2
                incoming_speed = max(
                    abs(self.player.velocity_x),
                    abs(self.player.x - previous_x),
                )
                self.player.velocity_x = incoming_speed * WALL_BOUNCE_FACTOR

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
        if (
            self.pause_screen.visible
            or self.win_screen.visible
            or self.leaderboard_screen.visible
            or self.settings_screen.visible
            or self.start_screen.visible
        ):
            return

        self.background_renderer.update(delta_time)
        self.particles.update(delta_time)
        self.slide_particle_timer -= delta_time

        self.elapsed_time += delta_time

        if self.camera.transitioning:
            self.update_camera_transition(delta_time)
            return

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
            blockers = self.walls + self.boundary_walls + self.slopes + [
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

        self.check_win_condition()
        if self.win_screen.visible:
            self.player.sync_world_position()
            return

        current_level = self.level_manager.current_level
        level_bottom = current_level.world_offset_y
        level_top = level_bottom + SCREEN_HEIGHT

        if self.player.top < level_bottom:
            self.transition_to_adjacent_level(-1)

        elif self.player.bottom > level_top:
            # Level 10 has no higher screen. Let the player continue a normal
            # jump above the window instead of snapping them back or creating
            # an imaginary Level 11.
            if current_level.level_index < self.level_manager.total_levels - 1:
                self.transition_to_adjacent_level(1)
            else:
                self.player.sync_world_position()

        else:
            self.player.sync_world_position()

    def on_draw(self):
        """Draw all game objects."""
        self.camera.use_screen()
        self.clear((7, 14, 28))

        self.background_renderer.draw(self.level_manager.current_level_number)
        self.structure_renderer.draw(self.level_manager.current_level_number)

        self.camera.use_world()

        for wall in self.previous_walls:
            wall.draw()

        for slope in self.previous_slopes:
            slope.draw()

        for platform in self.previous_platforms:
            platform.draw()

        for wall in self.walls:
            wall.draw()

        for slope in self.slopes:
            slope.draw()

        for platform in self.platforms:
            platform.draw()

        self.particles.draw()
        self.player.draw()

        self.camera.use_screen()
        self.draw_hud()
        self.start_screen.draw()
        self.win_screen.draw()
        self.leaderboard_screen.draw()
        self.settings_screen.draw()
        self.pause_screen.draw()

    def draw_hud(self):
        """Draw compact interface information above the game world."""
        level_number = self.level_manager.current_level_number
        total_levels = self.level_manager.total_levels

        if not self.settings_store.get("show_hud"):
            if self.settings_store.get("show_control_hints"):
                self.controls_text.draw()
            return

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
        arcade.draw_lbwh_rectangle_filled(
            210,
            SCREEN_HEIGHT - 48,
            190,
            32,
            (14, 22, 40, 190),
        )
        arcade.draw_lbwh_rectangle_outline(
            210,
            SCREEN_HEIGHT - 48,
            190,
            32,
            (143, 211, 191),
            1,
        )
        self.level_text.text = f"LEVEL {level_number:02d} / {total_levels:02d}"
        self.title_text.draw()
        self.level_text.draw()

        self.stats_text.text = (
            f"TIME {self.formatted_elapsed_time()}   JUMPS {self.jump_count:03d}"
        )
        self.stats_text.draw()

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
        if self.settings_store.get("show_control_hints"):
            self.controls_text.draw()
