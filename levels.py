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
        # Level 1 introduces the tower spine with broad landings and one
        # gentle return through the upper window.
        {"center_x": 400, "center_y": 70, "width": 210, "height": 12},
        {"center_x": 350, "center_y": 155, "width": 110, "height": 12},
        {"center_x": 520, "center_y": 245, "width": 100, "height": 12},
        {"center_x": 610, "center_y": 320, "width": 90, "height": 11},
        {"center_x": 500, "center_y": 395, "width": 90, "height": 11},
        {"center_x": 620, "center_y": 445, "width": 70, "height": 11},
        # This platform matches level 2's first platform.
        {"center_x": 680, "center_y": 550, "width": 65, "height": 11},
    ]

    level_one_walls = [
        # One central wall spine runs through the whole tower. These openings
        # are wide and forgiving so Level 1 teaches the barrier language.
        {
            "center_x": 430,
            "width": 32,
            "openings": [(0, 175), (195, 265), (350, 500)],
            "segment_offsets": [0, 10, -7],
            "segment_widths": [44, 28, 38],
            "cross_braces": [
                {"center_x": 190, "center_y": 220, "width": 220, "height": 12},
            ],
        },
    ]

    # Level 1 intentionally has no slopes.
    level_one_slopes = []

    level_two = [
        # Level 2 makes the first meaningful wall-window transfer: right,
        # through the center, left, then back through the upper window.
        {"center_x": 680, "center_y": 70, "width": 80, "height": 11},
        {"center_x": 600, "center_y": 150, "width": 70, "height": 11},
        {
            "center_x": 500,
            "center_y": 230,
            "width": 58,
            "height": 11,
            "movement_range_x": 30,
            "speed": 0.42,
        },
        {"center_x": 340, "center_y": 190, "width": 52, "height": 10},
        {"center_x": 280, "center_y": 310, "width": 48, "height": 10},
        # A central staging landing turns the long lower transfer into two
        # readable jumps through the same wall window.
        {"center_x": 400, "center_y": 350, "width": 42, "height": 10},
        {
            "center_x": 520,
            "center_y": 390,
            "width": 44,
            "height": 10,
            "movement_range_x": 28,
            "speed": 0.4,
        },
        {"center_x": 550, "center_y": 470, "width": 44, "height": 10},
        {"center_x": 350, "center_y": 500, "width": 50, "height": 10},
        # This platform matches level 3's first platform.
        {"center_x": 180, "center_y": 550, "width": 65, "height": 11},
    ]

    level_two_walls = [
        # The spine drifts right and thickens. The upper window is the only
        # route back into the left chamber.
        {
            "center_x": 460,
            "width": 38,
            "openings": [(145, 265), (360, 520)],
            "segment_offsets": [-8, 9],
            "segment_widths": [48, 34],
            "cross_braces": [
                {"center_x": 180, "center_y": 270, "width": 220, "height": 12},
                {"center_x": 635, "center_y": 425, "width": 200, "height": 12},
            ],
        },
    ]

    level_two_slopes = [
        # This downhill-left slope is the intentional dip from P4 to P5.
        {"start_x": 430, "start_y": 215, "end_x": 380, "end_y": 170},
    ]

    level_three = [
        # Level 3 crosses the drifting spine three times, with lower windows
        # requiring the player to reverse before the next landing.
        {"center_x": 180, "center_y": 70, "width": 65, "height": 11},
        {"center_x": 90, "center_y": 150, "width": 62, "height": 11},
        {
            "center_x": 260,
            "center_y": 100,
            "width": 50,
            "height": 10,
            "movement_range_x": 34,
            "speed": 0.45,
        },
        {"center_x": 350, "center_y": 220, "width": 46, "height": 10},
        {"center_x": 520, "center_y": 170, "width": 42, "height": 10},
        {
            "center_x": 470,
            "center_y": 300,
            "width": 38,
            "height": 10,
            "movement_range_x": 25,
            "speed": 0.4,
        },
        {"center_x": 330, "center_y": 360, "width": 36, "height": 10},
        {"center_x": 500, "center_y": 400, "width": 34, "height": 10},
        # A high-right setup landing makes the final transfer a continuation
        # of the window route instead of an isolated maximum-distance jump.
        {"center_x": 620, "center_y": 480, "width": 30, "height": 10},
        # This platform matches level 4's first platform.
        {"center_x": 720, "center_y": 550, "width": 55, "height": 11},
    ]

    level_three_walls = [
        # The spine bends left and uses two lower windows plus a high return.
        {
            "center_x": 410,
            "width": 34,
            "openings": [(120, 230), (250, 330), (350, 430)],
            "segment_offsets": [10, -8, 12],
            "segment_widths": [42, 28, 38],
            "cross_braces": [
                {"center_x": 180, "center_y": 275, "width": 220, "height": 12},
                {"center_x": 630, "center_y": 335, "width": 220, "height": 12},
            ],
        },
    ]

    # Level 3 deliberately removes slopes so moving platforms are the only
    # new focus after the level-two slope lesson.
    level_three_slopes = []

    level_four = [
        # Level 4 is a split-shaft lesson: the player crosses the wall near
        # the moving platform, then uses the slope to return through a low gap.
        {"center_x": 720, "center_y": 70, "width": 55, "height": 11},
        {"center_x": 620, "center_y": 160, "width": 48, "height": 10},
        {
            "center_x": 480,
            "center_y": 110,
            "width": 42,
            "height": 10,
            "movement_range_y": 24,
            "speed": 0.4,
        },
        {"center_x": 530, "center_y": 250, "width": 42, "height": 10},
        # This small landing sits above the lower window and sets up the
        # slope's leftward momentum transfer.
        {"center_x": 470, "center_y": 300, "width": 32, "height": 10},
        {"center_x": 350, "center_y": 390, "width": 42, "height": 10},
        {
            "center_x": 260,
            "center_y": 300,
            "width": 34,
            "height": 10,
            "movement_range_x": 24,
            "speed": 0.4,
        },
        {"center_x": 220, "center_y": 430, "width": 34, "height": 10},
        # This platform matches level 5's first platform.
        {"center_x": 180, "center_y": 550, "width": 50, "height": 11},
    ]

    level_four_walls = [
        # The spine drifts right and its lower window aligns with the slope.
        {
            "center_x": 455,
            "width": 42,
            "openings": [(70, 150), (260, 360), (400, 500)],
            "segment_offsets": [-10, 8, 12],
            "segment_widths": [50, 34, 44],
            "cross_braces": [
                {"center_x": 635, "center_y": 205, "width": 220, "height": 12},
                {"center_x": 190, "center_y": 350, "width": 220, "height": 12},
            ],
        },
    ]

    level_four_slopes = [
        # This uphill-left slope is the bridge from the low reset to P5.
        {"start_x": 430, "start_y": 285, "end_x": 350, "end_y": 370},
    ]

    level_five = [
        # Level 5 creates two opposing chambers connected by staggered
        # windows, with a moving platform guarding the upper return.
        {"center_x": 180, "center_y": 70, "width": 50, "height": 11},
        {"center_x": 300, "center_y": 155, "width": 46, "height": 10},
        # A center landing teaches the first window crossing before the
        # moving platform asks for timing.
        {"center_x": 400, "center_y": 105, "width": 38, "height": 10},
        {
            "center_x": 520,
            "center_y": 100,
            "width": 42,
            "height": 10,
            "movement_range_x": 28,
            "speed": 0.42,
        },
        {
            "center_x": 360,
            "center_y": 250,
            "width": 40,
            "height": 10,
            "movement_range_x": 30,
            "speed": 0.45,
        },
        {"center_x": 220, "center_y": 180, "width": 48, "height": 10},
        {"center_x": 350, "center_y": 340, "width": 36, "height": 10},
        # This reset landing separates the lower return from the next
        # moving-platform transfer.
        {"center_x": 390, "center_y": 370, "width": 36, "height": 10},
        {
            "center_x": 550,
            "center_y": 300,
            "width": 34,
            "height": 10,
            "movement_range_x": 28,
            "speed": 0.4,
        },
        {"center_x": 640, "center_y": 430, "width": 34, "height": 10},
        # This platform matches level 6's first platform.
        {"center_x": 700, "center_y": 550, "width": 45, "height": 11},
    ]

    level_five_walls = [
        # The spine bends left; its different segment thicknesses make the
        # lower return feel like a reinforced maintenance section.
        {
            "center_x": 430,
            "width": 34,
            "openings": [(80, 190), (260, 360), (420, 500)],
            "segment_offsets": [8, -10, 7],
            "segment_widths": [46, 30, 40],
            "cross_braces": [
                {"center_x": 175, "center_y": 245, "width": 210, "height": 12},
                {"center_x": 635, "center_y": 355, "width": 200, "height": 12},
            ],
        },
    ]

    # Level 5 reinforces walls and moving-platform timing without adding a
    # new slope challenge.
    level_five_slopes = []

    level_six = [
        # Level 6 makes a wide rightward return through the second window,
        # with the slope acting as a visible bridge toward that wall opening.
        {"center_x": 700, "center_y": 70, "width": 45, "height": 11},
        {"center_x": 600, "center_y": 160, "width": 42, "height": 10},
        {
            "center_x": 480,
            "center_y": 105,
            "width": 36,
            "height": 10,
            "movement_range_x": 35,
            "speed": 0.45,
        },
        # This landing breaks the nearly maximum-height transfer into a
        # controlled approach to the lower-left chamber.
        {"center_x": 400, "center_y": 220, "width": 34, "height": 10},
        {"center_x": 310, "center_y": 300, "width": 34, "height": 10},
        {"center_x": 230, "center_y": 190, "width": 38, "height": 10},
        # A middle landing makes the wide return to the upper-right mover a
        # two-beat momentum challenge instead of one blind leap.
        {"center_x": 350, "center_y": 270, "width": 34, "height": 10},
        {
            "center_x": 500,
            "center_y": 360,
            "width": 36,
            "height": 10,
            "movement_range_x": 30,
            "speed": 0.4,
        },
        {"center_x": 390, "center_y": 330, "width": 34, "height": 10},
        {"center_x": 270, "center_y": 300, "width": 32, "height": 10},
        {"center_x": 180, "center_y": 450, "width": 32, "height": 10},
        # This platform matches level 7's first platform.
        {"center_x": 210, "center_y": 550, "width": 42, "height": 11},
    ]

    level_six_walls = [
        # The spine shifts left and uses a broad lower window followed by a
        # reinforced upper section.
        {
            "center_x": 405,
            "width": 46,
            "openings": [(80, 380)],
            "segment_offsets": [8, -10],
            "segment_widths": [54, 36],
            "cross_braces": [
                {"center_x": 625, "center_y": 235, "width": 210, "height": 12},
                {"center_x": 175, "center_y": 370, "width": 200, "height": 12},
            ],
        },
    ]

    level_six_slopes = [
        # This short ramp gives the lower-left chamber a deliberate landing
        # line without occupying either of its nearby platforms.
        {"start_x": 205, "start_y": 205, "end_x": 300, "end_y": 280},
    ]

    level_seven = [
        # Level 7 uses the drifting spine as a window-to-window precision
        # test while moving platforms control the timing on the right side.
        {"center_x": 210, "center_y": 70, "width": 42, "height": 11},
        {"center_x": 350, "center_y": 160, "width": 38, "height": 10},
        {
            "center_x": 520,
            "center_y": 100,
            "width": 34,
            "height": 10,
            "movement_range_x": 40,
            "speed": 0.4,
        },
        {"center_x": 390, "center_y": 250, "width": 32, "height": 10},
        {"center_x": 540, "center_y": 180, "width": 30, "height": 10},
        # The first decision landing interrupts the predictable rightward
        # rhythm and gives the player a deliberate setup for the next jump.
        {"center_x": 600, "center_y": 275, "width": 30, "height": 10},
        {"center_x": 660, "center_y": 330, "width": 28, "height": 10},
        {
            "center_x": 540,
            "center_y": 270,
            "width": 28,
            "height": 10,
            "movement_range_x": 32,
            "speed": 0.4,
        },
        {"center_x": 600, "center_y": 350, "width": 30, "height": 10},
        {"center_x": 650, "center_y": 420, "width": 28, "height": 10},
        # This platform matches level 8's first platform.
        {"center_x": 720, "center_y": 550, "width": 38, "height": 11},
    ]

    level_seven_walls = [
        # The spine drifts right and leaves a single tall window for the
        # alternating left/right transfers.
        {
            "center_x": 465,
            "width": 32,
            "openings": [(100, 280), (390, 500)],
            "segment_offsets": [-8, 10],
            "segment_widths": [42, 30],
            "cross_braces": [
                {"center_x": 180, "center_y": 300, "width": 220, "height": 12},
                {"center_x": 645, "center_y": 245, "width": 240, "height": 12},
            ],
        },
    ]

    # Level 7 is a slope-free precision section before the steep-slope test.
    level_seven_slopes = []

    level_eight = [
        # Level 8 opens a second chamber on the right before the final
        # leftward return, making the slope and the windows one challenge.
        {"center_x": 720, "center_y": 70, "width": 38, "height": 11},
        {"center_x": 640, "center_y": 160, "width": 35, "height": 10},
        {
            "center_x": 520,
            "center_y": 105,
            "width": 32,
            "height": 10,
            "movement_range_x": 45,
            "speed": 0.4,
        },
        {"center_x": 380, "center_y": 260, "width": 30, "height": 10},
        {"center_x": 320, "center_y": 380, "width": 34, "height": 10},
        {
            "center_x": 220,
            "center_y": 300,
            "width": 29,
            "height": 10,
            "movement_range_x": 28,
            "speed": 0.4,
        },
        # This landing receives the slope momentum before the player crosses
        # the lower window into the right chamber.
        {"center_x": 440, "center_y": 365, "width": 32, "height": 10},
        {"center_x": 480, "center_y": 400, "width": 28, "height": 10},
        # The recovery landing makes the final leftward transfer readable.
        {"center_x": 390, "center_y": 450, "width": 30, "height": 10},
        {"center_x": 300, "center_y": 480, "width": 30, "height": 10},
        # This platform matches level 9's first platform.
        {"center_x": 180, "center_y": 550, "width": 35, "height": 11},
    ]

    level_eight_walls = [
        # The spine shifts left. A second upper window lets the player leave
        # the right chamber before the final recovery landing.
        {
            "center_x": 420,
            "width": 40,
            "openings": [(140, 300), (360, 500)],
            "segment_offsets": [10, -8],
            "segment_widths": [48, 34],
            "cross_braces": [
                {"center_x": 625, "center_y": 220, "width": 220, "height": 12},
                {"center_x": 170, "center_y": 365, "width": 200, "height": 12},
            ],
        },
    ]

    level_eight_slopes = [
        # A steep angle demands deliberate landing momentum and direction.
        {"start_x": 365, "start_y": 300, "end_x": 305, "end_y": 365},
    ]

    level_nine = [
        # Level 9 is a long precision route with a high return through a
        # second window, rather than a single diagonal staircase.
        {"center_x": 180, "center_y": 70, "width": 35, "height": 11},
        {"center_x": 320, "center_y": 160, "width": 34, "height": 10},
        {
            "center_x": 430,
            "center_y": 100,
            "width": 30,
            "height": 10,
            "movement_range_x": 55,
            "speed": 0.4,
        },
        {"center_x": 340, "center_y": 250, "width": 28, "height": 10},
        {"center_x": 500, "center_y": 180, "width": 27, "height": 10},
        # This left-of-spine landing keeps the high return inside the lower
        # window before the route turns toward the moving platform.
        {"center_x": 400, "center_y": 240, "width": 28, "height": 10},
        {"center_x": 360, "center_y": 380, "width": 26, "height": 10},
        {"center_x": 500, "center_y": 430, "width": 30, "height": 10},
        {
            "center_x": 620,
            "center_y": 300,
            "width": 27,
            "height": 10,
            "movement_range_x": 30,
            "speed": 0.4,
        },
        {"center_x": 680, "center_y": 430, "width": 26, "height": 10},
        # This platform matches level 10's first platform.
        {"center_x": 700, "center_y": 550, "width": 32, "height": 11},
    ]

    level_nine_walls = [
        # The spine bends right and leaves a lower window plus a high return
        # window for the final moving-platform transfer.
        {
            "center_x": 450,
            "width": 38,
            "openings": [(70, 280), (350, 500)],
            "segment_offsets": [-9, 10],
            "segment_widths": [48, 34],
            "cross_braces": [
                {"center_x": 180, "center_y": 300, "width": 220, "height": 12},
                {"center_x": 625, "center_y": 245, "width": 220, "height": 12},
            ],
        },
    ]

    level_nine_slopes = []

    level_ten = [
        # The summit is a compressed three-window sequence that ends in the
        # final leftward transfer through the tower's last opening.
        {"center_x": 700, "center_y": 70, "width": 32, "height": 11},
        {"center_x": 590, "center_y": 160, "width": 32, "height": 10},
        {
            "center_x": 480,
            "center_y": 105,
            "width": 28,
            "height": 10,
            "movement_range_x": 55,
            "speed": 0.4,
        },
        # This landing is the final window-crossing checkpoint before the
        # summit's tighter leftward route.
        {"center_x": 400, "center_y": 170, "width": 28, "height": 10},
        {"center_x": 340, "center_y": 270, "width": 27, "height": 10},
        {"center_x": 280, "center_y": 390, "width": 26, "height": 10},
        {
            "center_x": 500,
            "center_y": 360,
            "width": 24,
            "height": 10,
            "movement_range_x": 24,
            "speed": 0.4,
        },
        # A central recovery landing turns the long lower reversal into a
        # readable two-stage approach to the final moving platform.
        {"center_x": 380, "center_y": 330, "width": 28, "height": 10},
        {"center_x": 250, "center_y": 400, "width": 24, "height": 10},
        # The last small landing gives the player one controlled setup jump
        # before the final platform and the next-level seam.
        {"center_x": 180, "center_y": 480, "width": 28, "height": 10},
        # Final platform for the ten-level climb.
        {"center_x": 120, "center_y": 550, "width": 30, "height": 11},
    ]

    level_ten_walls = [
        # The summit spine shifts left and changes thickness at each window.
        {
            "center_x": 420,
            "width": 44,
            "openings": [(80, 190), (250, 380), (450, 540)],
            "segment_offsets": [10, -12, 8],
            "segment_widths": [52, 34, 46],
            "cross_braces": [
                {"center_x": 620, "center_y": 225, "width": 240, "height": 12},
                {"center_x": 170, "center_y": 440, "width": 190, "height": 12},
            ],
        },
    ]

    level_ten_slopes = [
        # The final slope repeats the learned momentum redirect under
        # tighter landing constraints.
        {"start_x": 345, "start_y": 300, "end_x": 290, "end_y": 370},
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
