"""The player character and player movement behavior."""

import math

import arcade

from settings import (
    ACCELERATION,
    FRICTION,
    GRAVITY,
    JUMP_CHARGE_RATE,
    JUMP_CHARGE_STEER_ACCELERATION,
    JUMP_AIM_GUIDE_LENGTH,
    JUMP_BAR_BACKGROUND_COLOR,
    JUMP_BAR_COLOR,
    JUMP_BAR_GAP,
    JUMP_BAR_HEIGHT,
    JUMP_BAR_WIDTH,
    MAX_JUMP_SPEED,
    MAX_JUMP_ANGLE_DEGREES,
    MIN_JUMP_SPEED,
    MIN_JUMP_ANGLE_DEGREES,
    MAX_SPEED,
    PLAYER_COLOR,
    PLAYER_HEIGHT,
    PLAYER_START_Y,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLOPE_STATIC_FRICTION,
    SLOPE_SLIDE_FRICTION,
    VERTICAL_AIM_TOLERANCE,
)


PLAYER_BODY_COLOR = (224, 82, 101)
PLAYER_SHADOW_COLOR = (91, 35, 66)
PLAYER_HIGHLIGHT_COLOR = (255, 174, 138)
PLAYER_VISOR_COLOR = (44, 54, 88)
PLAYER_EYE_COLOR = (238, 255, 214)


class Player:
    """The controllable player character."""

    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = SCREEN_WIDTH / 2
        self.y = PLAYER_START_Y
        self.world_y = self.y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.jump_keys_held = set()
        self.jump_charge = 0
        self.left_pressed = False
        self.right_pressed = False
        self.current_slope = None
        self.slope_sliding = False
        self.mouse_x = self.x
        self.mouse_y = self.y + 100
        self.camera_offset_y = 0

    @property
    def left(self):
        """Return the player's left edge."""
        return self.x - self.width / 2

    @property
    def right(self):
        """Return the player's right edge."""
        return self.x + self.width / 2

    @property
    def bottom(self):
        """Return the player's bottom edge."""
        return self.y - self.height / 2

    @property
    def top(self):
        """Return the player's top edge."""
        return self.y + self.height / 2

    def press_left(self):
        """Start moving left."""
        self.left_pressed = True

    def release_left(self):
        """Stop moving left."""
        self.left_pressed = False

    def press_right(self):
        """Start moving right."""
        self.right_pressed = True

    def release_right(self):
        """Stop moving right."""
        self.right_pressed = False

    def press_jump(self, key):
        """Begin charging a mouse-controlled jump while grounded."""
        self.jump_keys_held.add(key)

    def release_jump(self, key, mouse_x=None, mouse_y=None):
        """Release a jump toward the current mouse-controlled angle."""
        self.jump_keys_held.discard(key)

        if mouse_x is not None and mouse_y is not None:
            self.set_mouse_position(mouse_x, mouse_y)

        if not self.jump_keys_held and self.on_ground:
            jump_speed = max(MIN_JUMP_SPEED, self.jump_charge)
            jump_angle = self.get_jump_angle()
            self.velocity_x = math.cos(jump_angle) * jump_speed
            self.velocity_y = math.sin(jump_angle) * jump_speed
            self.jump_charge = 0
            self.on_ground = False
            self.current_slope = None
            self.slope_sliding = False
        elif not self.on_ground:
            self.jump_charge = 0

    def set_mouse_position(self, mouse_x, mouse_y):
        """Remember the mouse position used to aim the next jump."""
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def get_jump_angle(self):
        """Return an upward launch angle based on the mouse position."""
        change_x = self.mouse_x - self.x
        screen_y = self.y - self.camera_offset_y
        change_y = self.mouse_y - screen_y

        if abs(change_x) <= VERTICAL_AIM_TOLERANCE and change_y > 0:
            return math.pi / 2

        # Use the actual cursor angle so small mouse movements create small
        # launch-angle changes. Downward cursor positions are clamped to the
        # shallowest upward angle instead of allowing downward jumps.
        if change_y <= 0:
            raw_angle = (
                0
                if change_x > 0
                else math.pi
            )
        else:
            raw_angle = math.atan2(change_y, change_x)

        minimum_angle = math.radians(MIN_JUMP_ANGLE_DEGREES)
        maximum_angle = math.radians(MAX_JUMP_ANGLE_DEGREES)
        return max(
            minimum_angle,
            min(maximum_angle, raw_angle),
        )

    def jump_aim_endpoint(self):
        """Return a short visual guide endpoint for the current aim."""
        angle = self.get_jump_angle()
        return (
            self.x + math.cos(angle) * JUMP_AIM_GUIDE_LENGTH,
            self.y + math.sin(angle) * JUMP_AIM_GUIDE_LENGTH,
        )

    def update_jump_charge(self):
        """Increase jump power while a jump key is held on the ground."""
        if self.on_ground and self.jump_keys_held:
            self.jump_charge = min(
                MAX_JUMP_SPEED,
                self.jump_charge + JUMP_CHARGE_RATE,
            )

    def update_horizontal_position(self):
        """Accelerate, slow down, and move horizontally."""
        if not self.on_ground:
            # A jump is committed at launch. Horizontal input cannot change
            # the trajectory until the player lands or hits a wall.
            self.x += self.velocity_x
            self.keep_inside_screen()
            return

        if self.jump_keys_held:
            # Charging does not move the player, but it can shape the launch
            # direction. This preserves the Jump King-style decision without
            # allowing the player to walk around while charging.
            if self.left_pressed and not self.right_pressed:
                self.velocity_x -= JUMP_CHARGE_STEER_ACCELERATION
            elif self.right_pressed and not self.left_pressed:
                self.velocity_x += JUMP_CHARGE_STEER_ACCELERATION
            else:
                self.velocity_x *= FRICTION
        elif self.left_pressed and not self.right_pressed:
            self.velocity_x -= ACCELERATION
        elif self.right_pressed and not self.left_pressed:
            self.velocity_x += ACCELERATION
        else:
            # Friction slows the player when no horizontal direction is held.
            friction = (
                SLOPE_SLIDE_FRICTION
                if self.current_slope and self.slope_sliding
                else FRICTION
            )
            self.velocity_x *= friction

        self.velocity_x = max(-MAX_SPEED, min(MAX_SPEED, self.velocity_x))
        if not self.jump_keys_held:
            self.x += self.velocity_x

        # Keep the player inside the left and right edges of the window.
        self.keep_inside_screen()

    def keep_inside_screen(self):
        """Keep the player inside the horizontal screen boundaries."""
        left_edge = self.width / 2
        right_edge = SCREEN_WIDTH - self.width / 2

        if self.x < left_edge:
            self.x = left_edge
            self.velocity_x = 0
        elif self.x > right_edge:
            self.x = right_edge
            self.velocity_x = 0

    def update_vertical_position(self):
        """Apply gravity and move vertically."""
        previous_bottom = self.bottom
        self.velocity_y -= GRAVITY
        self.y += self.velocity_y
        self.on_ground = False
        self.current_slope = None
        self.slope_sliding = False
        return previous_bottom

    def land_on(self, platform_top):
        """Place the player on top of a platform."""
        self.y = platform_top + self.height / 2
        self.velocity_y = 0
        self.on_ground = True
        self.current_slope = None
        self.slope_sliding = False

    def land_on_slope(self, slope, incoming_velocity_y):
        """Land on a slope and transfer falling momentum into it."""
        self.y = slope.surface_y_at(self.x) + self.height / 2
        self.velocity_y = 0
        self.on_ground = True
        self.current_slope = slope
        self.slope_sliding = False

        # Gravity points downward. Projecting the incoming downward speed
        # onto the slope sends the player toward the lower end of the slope.
        if abs(slope.tangent_x) > 0.001:
            self.velocity_x += incoming_velocity_y * slope.tangent_y / slope.tangent_x

    def update_slope_physics(self, slope):
        """Apply slope gravity and static friction to horizontal momentum."""
        if abs(slope.tangent_x) <= 0.001:
            return

        slope_force = -GRAVITY * slope.tangent_y / slope.tangent_x
        proposed_velocity = self.velocity_x + slope_force

        # Manual steering should move the player along the slope without
        # turning a normal walk into an automatic slide.
        if not self.slope_sliding and (self.left_pressed or self.right_pressed):
            return

        # Small momentum is absorbed by static friction. Larger momentum
        # overcomes it and turns the player into a sliding state.
        if (
            not self.slope_sliding
            and not self.left_pressed
            and not self.right_pressed
            and abs(proposed_velocity) <= SLOPE_STATIC_FRICTION
        ):
            self.velocity_x = 0
            return

        self.slope_sliding = True
        self.velocity_x = proposed_velocity

    def reset(self):
        """Return the player to the starting position."""
        self.x = SCREEN_WIDTH / 2
        self.y = PLAYER_START_Y
        self.world_y = self.y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.current_slope = None
        self.slope_sliding = False
        self.jump_keys_held.clear()
        self.jump_charge = 0

    def set_camera_offset(self, offset_y):
        """Tell the player where the camera currently views the world."""
        self.camera_offset_y = offset_y

    def sync_world_position(self, level_offset_y=0):
        """Keep the compatibility world-position value synced to physics."""
        self.world_y = self.y

    def draw(self):
        """Draw the player as a small expressive explorer character."""
        if self.jump_keys_held:
            aim_x, aim_y = self.jump_aim_endpoint()
            arcade.draw_line(
                self.x,
                self.y,
                aim_x,
                aim_y,
                (255, 225, 137, 170),
                2,
            )
            arcade.draw_circle_filled(
                aim_x,
                aim_y,
                2,
                (255, 241, 177, 210),
            )

        # A soft charge glow makes it clear that the player is preparing a
        # jump, especially against the darker upper-level backgrounds.
        if self.jump_charge > 0:
            glow_radius = 10 + self.jump_charge / MAX_JUMP_SPEED * 6
            arcade.draw_circle_filled(
                self.x,
                self.y,
                glow_radius,
                (255, 206, 105, 34),
            )

        # A small contact shadow helps the player read against platforms.
        if self.on_ground:
            shadow_width = max(5, min(14, 8 + abs(self.velocity_x)))
            arcade.draw_ellipse_filled(
                self.x,
                self.bottom - 2,
                shadow_width,
                3,
                (18, 24, 43, 100),
            )

        arcade.draw_lbwh_rectangle_filled(
            self.left + 2,
            self.bottom - 2,
            self.width,
            self.height,
            PLAYER_SHADOW_COLOR,
        )
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.bottom,
            self.width,
            self.height,
            PLAYER_BODY_COLOR,
        )
        arcade.draw_lbwh_rectangle_outline(
            self.left,
            self.bottom,
            self.width,
            self.height,
            PLAYER_COLOR,
            1,
        )

        # The visor and eye direction give the tiny character a readable face.
        visor_width = max(5, self.width - 5)
        arcade.draw_lbwh_rectangle_filled(
            self.x - visor_width / 2,
            self.y + 1,
            visor_width,
            4,
            PLAYER_VISOR_COLOR,
        )
        eye_direction = 1 if self.velocity_x >= 0 else -1
        arcade.draw_circle_filled(
            self.x + eye_direction * 2,
            self.y + 3,
            1,
            PLAYER_EYE_COLOR,
        )
        arcade.draw_line(
            self.left + 3,
            self.top - 2,
            self.right - 3,
            self.top - 2,
            PLAYER_HIGHLIGHT_COLOR,
            1,
        )

        # Show the power bar only while a jump is being prepared. Keeping it
        # contextual preserves the player's focus on the landing geometry.
        if self.jump_charge > 0 or self.jump_keys_held:
            bar_left = self.x - JUMP_BAR_WIDTH / 2
            bar_bottom = self.bottom - JUMP_BAR_GAP - JUMP_BAR_HEIGHT
            arcade.draw_lbwh_rectangle_filled(
                bar_left - 2,
                bar_bottom - 2,
                JUMP_BAR_WIDTH + 4,
                JUMP_BAR_HEIGHT + 4,
                (20, 27, 45, 150),
            )
            arcade.draw_lbwh_rectangle_filled(
                bar_left,
                bar_bottom,
                JUMP_BAR_WIDTH,
                JUMP_BAR_HEIGHT,
                JUMP_BAR_BACKGROUND_COLOR,
            )

            charge_ratio = self.jump_charge / MAX_JUMP_SPEED
            arcade.draw_lbwh_rectangle_filled(
                bar_left,
                bar_bottom,
                JUMP_BAR_WIDTH * charge_ratio,
                JUMP_BAR_HEIGHT,
                JUMP_BAR_COLOR,
            )
            arcade.draw_lbwh_rectangle_outline(
                bar_left,
                bar_bottom,
                JUMP_BAR_WIDTH,
                JUMP_BAR_HEIGHT,
                (255, 243, 186),
                1,
            )
