"""Shared game settings and constants."""

import arcade


# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simple Platformer"
LEVEL_HEIGHT = SCREEN_HEIGHT
CAMERA_SCROLL_SPEED = 1800

# Colors
BACKGROUND_COLOR = arcade.color.SKY_BLUE
PLAYER_COLOR = arcade.color.RED
PLATFORM_COLOR = arcade.color.DARK_GREEN
WALL_COLOR = arcade.color.DARK_BROWN

# Player settings
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
ACCELERATION = 0.4
MAX_SPEED = 4
FRICTION = 0.8
GRAVITY = 0.7
MIN_JUMP_SPEED = 7
# A full charge takes about 34 frames at 60 FPS. This gives the player a
# compact, repeatable timing window to learn instead of a long hold.
MAX_JUMP_SPEED = 17
JUMP_CHARGE_RATE = 0.5
JUMP_CHARGE_STEER_ACCELERATION = 0.2
# These are absolute screen-space launch angles. The full upward semicircle
# remains available, while the small tolerance makes straight-up aiming easy.
MIN_JUMP_ANGLE_DEGREES = 25
MAX_JUMP_ANGLE_DEGREES = 155
VERTICAL_AIM_TOLERANCE = 6
JUMP_AIM_GUIDE_LENGTH = 34
JUMP_BAR_WIDTH = 36
JUMP_BAR_HEIGHT = 5
JUMP_BAR_GAP = 5
JUMP_BAR_BACKGROUND_COLOR = arcade.color.DARK_GRAY
JUMP_BAR_COLOR = arcade.color.YELLOW
SLOPE_SLIDE_FRICTION = 0.75
SLOPE_STATIC_FRICTION = 0.75

# The starting platform is centered at y=70 and is 12 pixels tall.
PLAYER_START_Y = 83.5
