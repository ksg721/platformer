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
        # Level 1 teaches the basic rhythm: short setup, committed transfer,
        # reverse direction, then a calm approach to the level seam.
        # The climb begins on a left-side entry ledge, supported by the
        # buttress below it rather than sitting on a generic floor.
        {"center_x": 220, "center_y": 64, "width": 140, "height": 12},
        {"center_x": 350, "center_y": 155, "width": 140, "height": 12},
        {"center_x": 520, "center_y": 250, "width": 120, "height": 12},
        {"center_x": 650, "center_y": 350, "width": 110, "height": 11},
        {"center_x": 520, "center_y": 445, "width": 110, "height": 11},
        # This platform matches level 2's first platform exactly.
        {"center_x": 680, "center_y": 550, "width": 80, "height": 11},
    ]

    level_one_walls = [
        # Level 1 teaches the wall language with one long, low gate. The
        # player must cross beneath it before climbing onto the right side.
        {
            "center_x": 430,
            "width": 32,
            "openings": [(0, 300)],
            "segment_offsets": [0],
            "segment_widths": [46],
            "cross_braces": [],
        },
        {
            # This support meets the entry ledge at its left edge and runs to
            # the bottom of the room, making the starting space architectural.
            "center_x": 135,
            "center_y": 29,
            "width": 30,
            "height": 58,
        },
    ]

    # Level 1 intentionally has no slopes.
    level_one_slopes = []

    level_two = [
        # Level 2 keeps the seam landing from Level 1, then introduces one
        # moving setup, a controlled drop, and a wide return.
        {"center_x": 680, "center_y": 70, "width": 80, "height": 11},
        {"center_x": 590, "center_y": 155, "width": 85, "height": 11},
        {
            "center_x": 500,
            "center_y": 240,
            "width": 65,
            "height": 11,
            "movement_range_x": 30,
            "speed": 0.42,
        },
        {"center_x": 350, "center_y": 190, "width": 65, "height": 10},
        {"center_x": 270, "center_y": 315, "width": 65, "height": 10},
        # This landing is the recovery point after the first leftward
        # transfer and sets up the return through the upper opening.
        {"center_x": 500, "center_y": 410, "width": 65, "height": 10},
        {"center_x": 360, "center_y": 500, "width": 65, "height": 10},
        # This platform matches level 3's first platform.
        {"center_x": 180, "center_y": 550, "width": 65, "height": 11},
    ]

    level_two_walls = [
        # Two deliberate windows divide the route into three chambers. The
        # player crosses right-to-left through the lower window, then
        # left-to-right and right-to-left through the upper window.
        {
            "center_x": 430,
            "width": 38,
            "openings": [(120, 250), (300, 560)],
            "segment_offsets": [0, -8, 8],
            "segment_widths": [52, 38, 46],
            "cross_braces": [],
        },
    ]

    level_two_slopes = []

    level_three = [
        # Level 3 introduces longer transfers and one moving landing.
        {"center_x": 180, "center_y": 70, "width": 65, "height": 11},
        {"center_x": 90, "center_y": 160, "width": 70, "height": 11},
        {
            "center_x": 280,
            "center_y": 260,
            "width": 60,
            "height": 10,
            "movement_range_x": 34,
            "speed": 0.4,
        },
        {"center_x": 470, "center_y": 350, "width": 55, "height": 10},
        {"center_x": 620, "center_y": 440, "width": 50, "height": 10},
        {"center_x": 670, "center_y": 500, "width": 40, "height": 10},
        # This platform matches level 4's first platform.
        {"center_x": 720, "center_y": 550, "width": 55, "height": 11},
    ]

    level_three_walls = [
        # The solid spine closes the lower and upper shortcuts, leaving one
        # mid-height window for the level's single chamber crossing.
        {
            "center_x": 410,
            "width": 42,
            "openings": [(250, 380)],
            "segment_offsets": [8, -6],
            "segment_widths": [48, 38],
            "cross_braces": [],
        },
    ]

    # Level 3 deliberately keeps the focus on moving platforms and walls.
    level_three_slopes = []

    level_four = [
        # Level 4 turns the direction around and asks for longer leftward
        # transfers before the route settles at the next seam.
        {"center_x": 720, "center_y": 70, "width": 55, "height": 11},
        {"center_x": 600, "center_y": 160, "width": 55, "height": 10},
        {
            "center_x": 450,
            "center_y": 250,
            "width": 52,
            "height": 10,
            "movement_range_x": 30,
            "speed": 0.4,
        },
        {"center_x": 330, "center_y": 350, "width": 50, "height": 10},
        {"center_x": 220, "center_y": 445, "width": 48, "height": 10},
        {"center_x": 360, "center_y": 500, "width": 40, "height": 10},
        # This platform matches level 5's first platform.
        {"center_x": 180, "center_y": 550, "width": 50, "height": 11},
    ]

    level_four_walls = [
        # This gate sits between the opening right chamber and the left
        # route. Its single window makes the first transfer a clear choice.
        {
            "center_x": 520,
            "width": 50,
            "openings": [(120, 300)],
            "segment_offsets": [0, -8],
            "segment_widths": [56, 44],
            "cross_braces": [],
        },
    ]

    level_four_slopes = []

    level_five = [
        # Level 5 adds longer reversals and one moving landing.
        {"center_x": 180, "center_y": 70, "width": 50, "height": 11},
        {
            "center_x": 320,
            "center_y": 165,
            "width": 50,
            "height": 10,
        },
        {
            "center_x": 500,
            "center_y": 270,
            "width": 50,
            "height": 10,
            "movement_range_x": 35,
            "speed": 0.42,
        },
        {"center_x": 640, "center_y": 370, "width": 46, "height": 10},
        {"center_x": 520, "center_y": 460, "width": 44, "height": 10},
        {"center_x": 360, "center_y": 515, "width": 46, "height": 10},
        {"center_x": 520, "center_y": 520, "width": 44, "height": 10},
        # This platform matches level 6's first platform.
        {"center_x": 700, "center_y": 550, "width": 45, "height": 11},
    ]

    level_five_walls = [
        # The two windows separate the first rightward transfer from the
        # late return. The solid middle span makes the reversal intentional.
        {
            "center_x": 430,
            "width": 46,
            "openings": [(170, 330), (430, 550)],
            "segment_offsets": [0, 8, -6],
            "segment_widths": [52, 40, 48],
            "cross_braces": [],
        },
    ]

    # Level 5 reinforces walls and moving-platform timing without adding a
    # new slope challenge.
    level_five_slopes = []

    level_six = [
        # Level 6 asks for a long leftward route, one moving landing, and a
        # final reversal before the seam.
        {"center_x": 700, "center_y": 70, "width": 45, "height": 11},
        {"center_x": 560, "center_y": 170, "width": 45, "height": 10},
        {
            "center_x": 400,
            "center_y": 275,
            "width": 45,
            "height": 10,
            "movement_range_x": 35,
            "speed": 0.42,
        },
        {"center_x": 250, "center_y": 370, "width": 42, "height": 10},
        {"center_x": 380, "center_y": 450, "width": 40, "height": 10},
        {"center_x": 520, "center_y": 510, "width": 40, "height": 10},
        {"center_x": 350, "center_y": 530, "width": 40, "height": 10},
        # This platform matches level 7's first platform.
        {"center_x": 210, "center_y": 550, "width": 42, "height": 11},
    ]

    level_six_walls = [
        # Two windows create a measured left chamber, right chamber, and a
        # final return. The lower and middle wall spans block shortcuts.
        {
            "center_x": 405,
            "width": 46,
            "openings": [(150, 340), (400, 560)],
            "segment_offsets": [0, -8, 7],
            "segment_widths": [52, 40, 48],
            "cross_braces": [],
        },
    ]

    level_six_slopes = []

    level_seven = [
        # Level 7 uses tighter landings and a long final reversal.
        {"center_x": 210, "center_y": 70, "width": 42, "height": 11},
        {"center_x": 360, "center_y": 165, "width": 42, "height": 10},
        {
            "center_x": 540,
            "center_y": 270,
            "width": 40,
            "height": 10,
            "movement_range_x": 40,
            "speed": 0.4,
        },
        {"center_x": 680, "center_y": 370, "width": 38, "height": 10},
        {"center_x": 520, "center_y": 450, "width": 36, "height": 10},
        {"center_x": 360, "center_y": 515, "width": 36, "height": 10},
        {"center_x": 560, "center_y": 535, "width": 34, "height": 10},
        # This platform matches level 8's first platform.
        {"center_x": 720, "center_y": 550, "width": 38, "height": 11},
    ]

    level_seven_walls = [
        # The windows line up with the three side changes in this route,
        # while the intervening wall spans prevent straight-line shortcuts.
        {
            "center_x": 465,
            "width": 42,
            "openings": [(150, 320), (390, 560)],
            "segment_offsets": [0, 8, -7],
            "segment_widths": [48, 38, 44],
            "cross_braces": [],
        },
    ]

    # Level 7 is a slope-free precision section with tighter platforms.
    level_seven_slopes = []

    level_eight = [
        # Level 8 tightens the landing widths while keeping one moving
        # platform as the only extra timing element.
        {"center_x": 720, "center_y": 70, "width": 38, "height": 11},
        {"center_x": 600, "center_y": 165, "width": 40, "height": 10},
        {
            "center_x": 450,
            "center_y": 270,
            "width": 38,
            "height": 10,
            "movement_range_x": 40,
            "speed": 0.4,
        },
        {"center_x": 300, "center_y": 370, "width": 36, "height": 10},
        {"center_x": 450, "center_y": 455, "width": 34, "height": 10},
        {"center_x": 600, "center_y": 515, "width": 34, "height": 10},
        {"center_x": 330, "center_y": 535, "width": 34, "height": 10},
        # This platform matches level 9's first platform.
        {"center_x": 180, "center_y": 550, "width": 35, "height": 11},
    ]

    level_eight_walls = [
        # This offset spine forces the route to cross three intentional
        # windows instead of letting the player drift through the middle.
        {
            "center_x": 390,
            "width": 48,
            "openings": [(150, 440), (480, 560)],
            "segment_offsets": [0, -8, 8],
            "segment_widths": [54, 42, 50],
            "cross_braces": [],
        },
    ]

    level_eight_slopes = []

    level_nine = [
        # Level 9 uses narrow landings and long, deliberate reversals.
        {"center_x": 180, "center_y": 70, "width": 35, "height": 11},
        {"center_x": 330, "center_y": 165, "width": 36, "height": 10},
        {
            "center_x": 500,
            "center_y": 270,
            "width": 36,
            "height": 10,
            "movement_range_x": 50,
            "speed": 0.4,
        },
        {"center_x": 650, "center_y": 370, "width": 34, "height": 10},
        {"center_x": 500, "center_y": 455, "width": 34, "height": 10},
        {"center_x": 350, "center_y": 520, "width": 34, "height": 10},
        {"center_x": 520, "center_y": 535, "width": 32, "height": 10},
        # This platform matches level 10's first platform.
        {"center_x": 700, "center_y": 550, "width": 32, "height": 11},
    ]

    level_nine_walls = [
        # The precision route crosses the lower and upper windows; the solid
        # spans between them make each reversal a separate decision.
        {
            "center_x": 425,
            "width": 42,
            "openings": [(150, 320), (380, 580)],
            "segment_offsets": [0, 8, -7],
            "segment_widths": [48, 36, 44],
            "cross_braces": [],
        },
    ]

    level_nine_slopes = []

    level_ten = [
        # The summit uses the narrowest platforms and the longest final
        # transfer, without adding extra wall pieces.
        {"center_x": 700, "center_y": 70, "width": 32, "height": 11},
        {"center_x": 560, "center_y": 165, "width": 34, "height": 10},
        {
            "center_x": 400,
            "center_y": 270,
            "width": 34,
            "height": 10,
            "movement_range_x": 50,
            "speed": 0.4,
        },
        {"center_x": 250, "center_y": 380, "width": 32, "height": 10},
        {"center_x": 400, "center_y": 465, "width": 30, "height": 10},
        {"center_x": 560, "center_y": 520, "width": 30, "height": 10},
        {"center_x": 370, "center_y": 540, "width": 30, "height": 10},
        # Final platform for the ten-level climb.
        {"center_x": 120, "center_y": 550, "width": 30, "height": 11},
    ]

    level_ten_walls = [
        # The summit has two narrow windows. The upper span closes the easy
        # center line and makes the final return a deliberate commitment.
        {
            "center_x": 420,
            "width": 44,
            "openings": [(150, 350), (400, 580)],
            "segment_offsets": [0, -8, 7],
            "segment_widths": [50, 38, 46],
            "cross_braces": [],
        },
    ]

    level_ten_slopes = []

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
