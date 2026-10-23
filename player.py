"""The player character and player movement behavior."""

import arcade

from settings import (
    ACCELERATION,
    FRICTION,
    GRAVITY,
    JUMP_CHARGE_RATE,
    JUMP_BAR_BACKGROUND_COLOR,
    JUMP_BAR_COLOR,
    JUMP_BAR_GAP,
    JUMP_BAR_HEIGHT,
    JUMP_BAR_WIDTH,
    MAX_JUMP_SPEED,
    MIN_JUMP_SPEED,
    MAX_SPEED,
    PLAYER_COLOR,
    PLAYER_HEIGHT,
    PLAYER_START_Y,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


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
        """Begin charging a jump while the player is grounded."""
        self.jump_keys_held.add(key)

    def release_jump(self, key):
        """Release a jump and launch using the stored charge."""
        self.jump_keys_held.discard(key)

        if not self.jump_keys_held and self.on_ground:
            self.velocity_y = max(MIN_JUMP_SPEED, self.jump_charge)
            self.jump_charge = 0
            self.on_ground = False
        elif not self.on_ground:
            self.jump_charge = 0

    def update_jump_charge(self):
        """Increase jump power while a jump key is held on the ground."""
        if self.on_ground and self.jump_keys_held:
            self.jump_charge = min(
                MAX_JUMP_SPEED,
                self.jump_charge + JUMP_CHARGE_RATE,
            )

    def update_horizontal_position(self):
        """Accelerate, slow down, and move horizontally."""
        if self.jump_keys_held:
            self.velocity_x = 0
            return

        if self.left_pressed and not self.right_pressed:
            self.velocity_x -= ACCELERATION
        elif self.right_pressed and not self.left_pressed:
            self.velocity_x += ACCELERATION
        else:
            # Friction slows the player when no horizontal direction is held.
            self.velocity_x *= FRICTION

        self.velocity_x = max(-MAX_SPEED, min(MAX_SPEED, self.velocity_x))
        self.x += self.velocity_x

        # Keep the player inside the left and right edges of the window.
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
        return previous_bottom

    def land_on(self, platform_top):
        """Place the player on top of a platform."""
        self.y = platform_top + self.height / 2
        self.velocity_y = 0
        self.on_ground = True

    def reset(self):
        """Return the player to the starting position."""
        self.x = SCREEN_WIDTH / 2
        self.y = PLAYER_START_Y
        self.world_y = self.y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.jump_keys_held.clear()
        self.jump_charge = 0

    def sync_world_position(self, level_offset_y):
        """Update world-space height from the current screen-space height."""
        self.world_y = self.y + level_offset_y

    def draw(self):
        """Draw the player."""
        arcade.draw_lbwh_rectangle_filled(
            self.left,
            self.bottom,
            self.width,
            self.height,
            PLAYER_COLOR,
        )

        # Draw the jump-power bar directly below the player.
        bar_left = self.x - JUMP_BAR_WIDTH / 2
        bar_bottom = self.bottom - JUMP_BAR_GAP - JUMP_BAR_HEIGHT
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
