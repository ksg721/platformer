"""Definitions for the game's platform levels."""

from level import Level
from settings import PLAYER_HEIGHT, PLAYER_START_Y, SCREEN_WIDTH


def create_levels():
    """Return the levels currently available in the game."""
    first_level_platforms = [
        # Level 1 is a wide, linear tutorial route.
        {"center_x": SCREEN_WIDTH / 2, "center_y": 70, "width": 220, "height": 12},
        {"center_x": 360, "center_y": 145, "width": 90, "height": 12},
        {"center_x": 300, "center_y": 220, "width": 80, "height": 12},
        {"center_x": 360, "center_y": 295, "width": 70, "height": 11},
        {"center_x": 450, "center_y": 370, "width": 75, "height": 11},
        {"center_x": 550, "center_y": 445, "width": 65, "height": 11},
        # This platform matches level 2's first platform.
        {"center_x": 680, "center_y": 550, "width": 65, "height": 11},
    ]

    second_level_platforms = [
        # This platform matches level 1's final platform.
        {"center_x": 680, "center_y": 70, "width": 65, "height": 11},
        {"center_x": 600, "center_y": 140, "width": 70, "height": 11},
        {
            "center_x": 540,
            "center_y": 210,
            "width": 65,
            "height": 11,
            "movement_range_x": 50,
            "speed": 0.75,
        },
        {"center_x": 470, "center_y": 285, "width": 60, "height": 10},
        {
            "center_x": 390,
            "center_y": 360,
            "width": 60,
            "height": 11,
            "movement_range_y": 35,
            "speed": 0.5,
        },
        {
            "center_x": 300,
            "center_y": 435,
            "width": 55,
            "height": 10,
            "movement_range_x": 45,
            "speed": 0.75,
        },
        {"center_x": 180, "center_y": 550, "width": 65, "height": 11},
    ]

    return [
        Level(
            platform_data=first_level_platforms,
            start_x=SCREEN_WIDTH / 2,
            start_y=PLAYER_START_Y,
            level_index=0,
        ),
        Level(
            platform_data=second_level_platforms,
            start_x=680,
            start_y=70 + 11 / 2 + PLAYER_HEIGHT / 2,
            level_index=1,
        ),
    ]
