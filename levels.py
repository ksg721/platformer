"""Definitions for the game's platform levels."""

from level import Level
from settings import PLAYER_HEIGHT


def make_level(platform_data, level_index, wall_data=None, slope_data=None):
    """Create a Level using its first platform as the starting platform."""
    starting_platform = platform_data[0]
    start_y = (
        starting_platform["center_y"]
        + starting_platform["height"] / 2
        + PLAYER_HEIGHT / 2
    )

    return Level(
        platform_data=platform_data,
        start_x=starting_platform["center_x"],
        start_y=start_y,
        level_index=level_index,
        wall_data=wall_data,
        slope_data=slope_data,
    )


def create_levels():
    """Return all ten levels in increasing difficulty order."""
    level_one = [
        # Level 1 beat 1: learn the charge jump with almost no steering.
        {"center_x": 400, "center_y": 70, "width": 220, "height": 12},
        {"center_x": 400, "center_y": 145, "width": 150, "height": 12},
        # Beat 2: one forgiving lateral jump.
        {"center_x": 500, "center_y": 220, "width": 110, "height": 12},
        {"center_x": 600, "center_y": 295, "width": 100, "height": 11},
        # Beat 3: reverse direction while the platforms remain generous.
        {"center_x": 500, "center_y": 370, "width": 95, "height": 11},
        {"center_x": 650, "center_y": 445, "width": 75, "height": 11},
        # This platform matches level 2's first platform.
        {"center_x": 680, "center_y": 550, "width": 65, "height": 11},
    ]

    level_one_walls = [
        # Walls are placed beside, not on, the tutorial landings.
        {"center_x": 450, "center_y": 180, "width": 16, "height": 40},
        {"center_x": 560, "center_y": 255, "width": 16, "height": 45},
        {"center_x": 460, "center_y": 405, "width": 16, "height": 50},
    ]

    # Level 1 intentionally has no slopes.
    level_one_slopes = []

    level_two = [
        # Level 2 beat 1: begin from the previous transition and add timing.
        {"center_x": 680, "center_y": 70, "width": 65, "height": 11},
        {"center_x": 600, "center_y": 140, "width": 70, "height": 11},
        {
            "center_x": 520,
            "center_y": 220,
            "width": 70,
            "height": 11,
            "movement_range_x": 28,
            "speed": 0.5,
        },
        # Beat 2: land on the slope, then use its direction to reach P5.
        {"center_x": 450, "center_y": 295, "width": 62, "height": 10},
        {"center_x": 410, "center_y": 390, "width": 52, "height": 10},
        {
            "center_x": 300,
            "center_y": 470,
            "width": 48,
            "height": 11,
            "movement_range_x": 20,
            "speed": 0.4,
        },
        # This platform matches level 3's first platform.
        {"center_x": 180, "center_y": 550, "width": 65, "height": 11},
    ]

    level_two_walls = [
        # The walls frame the intended approach to the moving platforms.
        {"center_x": 650, "center_y": 110, "width": 18, "height": 50},
        {"center_x": 550, "center_y": 260, "width": 18, "height": 65},
        {"center_x": 365, "center_y": 430, "width": 18, "height": 55},
    ]

    level_two_slopes = [
        # The first slope is a wide, forgiving landing that teaches sliding.
        {"start_x": 350, "start_y": 315, "end_x": 430, "end_y": 360},
    ]

    level_three = [
        # Level 3: a moving-platform lesson with no slope distraction.
        {"center_x": 180, "center_y": 70, "width": 65, "height": 11},
        {"center_x": 260, "center_y": 150, "width": 60, "height": 11},
        {
            "center_x": 400,
            "center_y": 230,
            "width": 52,
            "height": 10,
            "movement_range_x": 35,
            "speed": 0.45,
        },
        {"center_x": 300, "center_y": 310, "width": 48, "height": 10},
        {"center_x": 450, "center_y": 390, "width": 44, "height": 10},
        {
            "center_x": 600,
            "center_y": 470,
            "width": 40,
            "height": 10,
            "movement_range_x": 28,
            "speed": 0.4,
        },
        # This platform matches level 4's first platform.
        {"center_x": 720, "center_y": 550, "width": 55, "height": 11},
    ]

    level_three_walls = [
        {"center_x": 220, "center_y": 205, "width": 16, "height": 55},
        {"center_x": 370, "center_y": 350, "width": 16, "height": 60},
        {"center_x": 550, "center_y": 510, "width": 16, "height": 55},
    ]

    # Level 3 deliberately removes slopes so moving platforms are the only
    # new focus after the level-two slope lesson.
    level_three_slopes = []

    level_four = [
        # Level 4: a slope-landing test after the moving-platform lesson.
        {"center_x": 720, "center_y": 70, "width": 55, "height": 11},
        {"center_x": 650, "center_y": 140, "width": 50, "height": 10},
        {
            "center_x": 560,
            "center_y": 220,
            "width": 44,
            "height": 10,
            "movement_range_y": 20,
            "speed": 0.4,
        },
        {"center_x": 470, "center_y": 300, "width": 40, "height": 10},
        {"center_x": 400, "center_y": 395, "width": 38, "height": 10},
        {
            "center_x": 290,
            "center_y": 475,
            "width": 36,
            "height": 10,
            "movement_range_x": 24,
            "speed": 0.4,
        },
        # This platform matches level 5's first platform.
        {"center_x": 180, "center_y": 550, "width": 50, "height": 11},
    ]

    level_four_walls = [
        {"center_x": 690, "center_y": 105, "width": 16, "height": 48},
        {"center_x": 610, "center_y": 270, "width": 18, "height": 70},
        {"center_x": 445, "center_y": 360, "width": 18, "height": 65},
        {"center_x": 235, "center_y": 520, "width": 16, "height": 55},
    ]

    level_four_slopes = [
        # This slope is the intended landing before the lower moving platform.
        {"start_x": 360, "start_y": 325, "end_x": 430, "end_y": 375},
    ]

    level_five = [
        # Level 5: a slope-free consolidation level with a long rightward
        # rhythm and two moving-platform timing checks.
        {"center_x": 180, "center_y": 70, "width": 50, "height": 11},
        {"center_x": 260, "center_y": 145, "width": 46, "height": 10},
        {
            "center_x": 360,
            "center_y": 225,
            "width": 42,
            "height": 10,
            "movement_range_x": 32,
            "speed": 0.45,
        },
        {"center_x": 470, "center_y": 310, "width": 40, "height": 10},
        {"center_x": 550, "center_y": 395, "width": 38, "height": 10},
        {
            "center_x": 625,
            "center_y": 475,
            "width": 36,
            "height": 10,
            "movement_range_x": 24,
            "speed": 0.4,
        },
        # This platform matches level 6's first platform.
        {"center_x": 700, "center_y": 550, "width": 45, "height": 11},
    ]

    level_five_walls = [
        {"center_x": 220, "center_y": 108, "width": 16, "height": 45},
        {"center_x": 420, "center_y": 270, "width": 18, "height": 55},
        {"center_x": 590, "center_y": 440, "width": 16, "height": 45},
    ]

    # Level 5 reinforces walls and moving-platform timing without adding a
    # new slope challenge.
    level_five_slopes = []

    level_six = [
        # Level 6: the first deliberate momentum-redirecting slope.
        {"center_x": 700, "center_y": 70, "width": 45, "height": 11},
        {"center_x": 620, "center_y": 145, "width": 42, "height": 10},
        {
            "center_x": 520,
            "center_y": 225,
            "width": 38,
            "height": 10,
            "movement_range_x": 38,
            "speed": 0.45,
        },
        {"center_x": 430, "center_y": 310, "width": 36, "height": 10},
        {"center_x": 260, "center_y": 405, "width": 38, "height": 10},
        {
            "center_x": 190,
            "center_y": 485,
            "width": 34,
            "height": 10,
            "movement_range_x": 22,
            "speed": 0.4,
        },
        # This platform matches level 7's first platform.
        {"center_x": 210, "center_y": 550, "width": 42, "height": 11},
    ]

    level_six_walls = [
        {"center_x": 660, "center_y": 110, "width": 16, "height": 45},
        {"center_x": 490, "center_y": 275, "width": 18, "height": 65},
        {"center_x": 315, "center_y": 450, "width": 16, "height": 55},
    ]

    level_six_slopes = [
        # The downward-left angle carries momentum toward the next platform.
        {"start_x": 365, "start_y": 330, "end_x": 285, "end_y": 385},
    ]

    level_seven = [
        # Level 7: a slope-free precision section with changing rhythm.
        {"center_x": 210, "center_y": 70, "width": 42, "height": 11},
        {"center_x": 300, "center_y": 145, "width": 40, "height": 10},
        {
            "center_x": 430,
            "center_y": 225,
            "width": 36,
            "height": 10,
            "movement_range_x": 45,
            "speed": 0.4,
        },
        {"center_x": 520, "center_y": 310, "width": 34, "height": 10},
        {"center_x": 650, "center_y": 400, "width": 32, "height": 10},
        {
            "center_x": 690,
            "center_y": 485,
            "width": 30,
            "height": 10,
            "movement_range_y": 34,
            "speed": 0.4,
        },
        # This platform matches level 8's first platform.
        {"center_x": 720, "center_y": 550, "width": 38, "height": 11},
    ]

    level_seven_walls = [
        {"center_x": 260, "center_y": 110, "width": 16, "height": 45},
        {"center_x": 470, "center_y": 275, "width": 18, "height": 65},
        {"center_x": 610, "center_y": 445, "width": 16, "height": 55},
    ]

    # Level 7 is a slope-free precision section before the steep-slope test.
    level_seven_slopes = []

    level_eight = [
        # Level 8: the steep-slope momentum test.
        {"center_x": 720, "center_y": 70, "width": 38, "height": 11},
        {"center_x": 640, "center_y": 145, "width": 35, "height": 10},
        {
            "center_x": 550,
            "center_y": 225,
            "width": 32,
            "height": 10,
            "movement_range_x": 55,
            "speed": 0.4,
        },
        {"center_x": 460, "center_y": 310, "width": 30, "height": 10},
        {"center_x": 350, "center_y": 410, "width": 34, "height": 10},
        {
            "center_x": 250,
            "center_y": 490,
            "width": 29,
            "height": 10,
            "movement_range_x": 35,
            "speed": 0.4,
        },
        # This platform matches level 9's first platform.
        {"center_x": 180, "center_y": 550, "width": 35, "height": 11},
    ]

    level_eight_walls = [
        {"center_x": 690, "center_y": 110, "width": 16, "height": 45},
        {"center_x": 515, "center_y": 275, "width": 18, "height": 65},
        {"center_x": 300, "center_y": 455, "width": 16, "height": 55},
    ]

    level_eight_slopes = [
        # A steeper angle demands deliberate landing momentum.
        {"start_x": 400, "start_y": 330, "end_x": 330, "end_y": 395},
    ]

    level_nine = [
        # Level 9: a slope-free precision exam before the final combination.
        {"center_x": 180, "center_y": 70, "width": 35, "height": 11},
        {"center_x": 250, "center_y": 145, "width": 32, "height": 10},
        {
            "center_x": 350,
            "center_y": 225,
            "width": 30,
            "height": 10,
            "movement_range_x": 65,
            "speed": 0.4,
        },
        {"center_x": 440, "center_y": 310, "width": 28, "height": 10},
        {"center_x": 540, "center_y": 400, "width": 27, "height": 10},
        {
            "center_x": 640,
            "center_y": 490,
            "width": 27,
            "height": 10,
            "movement_range_x": 38,
            "speed": 0.4,
        },
        # This platform matches level 10's first platform.
        {"center_x": 700, "center_y": 550, "width": 32, "height": 11},
    ]

    level_nine_walls = [
        {"center_x": 220, "center_y": 110, "width": 16, "height": 45},
        {"center_x": 405, "center_y": 275, "width": 18, "height": 65},
        {"center_x": 590, "center_y": 455, "width": 16, "height": 55},
    ]

    level_nine_slopes = []

    level_ten = [
        # Level 10: the final authored sequence, combining every learned beat.
        {"center_x": 700, "center_y": 70, "width": 32, "height": 11},
        {"center_x": 620, "center_y": 145, "width": 30, "height": 10},
        {
            "center_x": 520,
            "center_y": 225,
            "width": 28,
            "height": 10,
            "movement_range_x": 65,
            "speed": 0.4,
        },
        {"center_x": 430, "center_y": 310, "width": 27, "height": 10},
        {"center_x": 350, "center_y": 410, "width": 26, "height": 10},
        {
            "center_x": 240,
            "center_y": 490,
            "width": 25,
            "height": 10,
            "movement_range_x": 30,
            "speed": 0.4,
        },
        # Final platform for the ten-level climb.
        {"center_x": 120, "center_y": 550, "width": 30, "height": 11},
    ]

    level_ten_walls = [
        {"center_x": 665, "center_y": 110, "width": 16, "height": 45},
        {"center_x": 490, "center_y": 275, "width": 18, "height": 65},
        {"center_x": 300, "center_y": 455, "width": 16, "height": 55},
    ]

    level_ten_slopes = [
        # The final slope repeats the learned momentum redirect under
        # tighter landing constraints.
        {"start_x": 375, "start_y": 330, "end_x": 425, "end_y": 395},
    ]

    return [
        make_level(level_one, 0, level_one_walls, level_one_slopes),
        make_level(level_two, 1, level_two_walls, level_two_slopes),
        make_level(level_three, 2, level_three_walls, level_three_slopes),
        make_level(level_four, 3, level_four_walls, level_four_slopes),
        make_level(level_five, 4, level_five_walls, level_five_slopes),
        make_level(level_six, 5, level_six_walls, level_six_slopes),
        make_level(level_seven, 6, level_seven_walls, level_seven_slopes),
        make_level(level_eight, 7, level_eight_walls, level_eight_slopes),
        make_level(level_nine, 8, level_nine_walls, level_nine_slopes),
        make_level(level_ten, 9, level_ten_walls, level_ten_slopes),
    ]
