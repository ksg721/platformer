"""Reusable visual effects for the platformer.

The game keeps its collision geometry separate from its artwork. That lets us
make the game look more detailed without changing the carefully tuned physics.
"""

import math

import arcade

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


def blend_color(first, second, amount):
    """Return a color between two RGB or RGBA colors."""
    amount = max(0.0, min(1.0, amount))
    return tuple(
        int(first[index] + (second[index] - first[index]) * amount)
        for index in range(len(first))
    )


class BackgroundRenderer:
    """Draw a layered background that changes as the player climbs."""

    THEMES = (
        {
            "top": (39, 48, 91),
            "bottom": (155, 111, 147),
            "sun": (255, 198, 128),
            "far": (72, 72, 119),
            "near": (39, 46, 83),
            "mist": (193, 165, 191),
            "accent": (255, 218, 150),
        },
        {
            "top": (21, 68, 104),
            "bottom": (79, 156, 169),
            "sun": (255, 229, 154),
            "far": (45, 104, 126),
            "near": (24, 63, 91),
            "mist": (148, 205, 196),
            "accent": (237, 255, 195),
        },
        {
            "top": (32, 42, 78),
            "bottom": (100, 83, 129),
            "sun": (255, 174, 123),
            "far": (57, 62, 105),
            "near": (29, 35, 68),
            "mist": (146, 137, 173),
            "accent": (255, 202, 137),
        },
        {
            "top": (17, 26, 58),
            "bottom": (61, 74, 121),
            "sun": (185, 216, 255),
            "far": (36, 55, 91),
            "near": (17, 28, 56),
            "mist": (111, 134, 175),
            "accent": (180, 226, 255),
        },
    )

    def __init__(self):
        self.time = 0.0

    def update(self, delta_time):
        """Advance the subtle background motion."""
        self.time += min(delta_time, 0.1)

    def draw(self, level_number):
        """Draw the sky, distant scenery, and atmospheric layers."""
        theme = self.THEMES[(level_number - 1) % len(self.THEMES)]

        # Horizontal bands create a soft gradient without requiring an image
        # file, so the project remains easy to run on another computer.
        band_height = SCREEN_HEIGHT / 12
        for band in range(12):
            amount = band / 11
            color = blend_color(theme["bottom"], theme["top"], amount)
            arcade.draw_lbwh_rectangle_filled(
                0,
                band * band_height,
                SCREEN_WIDTH,
                band_height + 1,
                color,
            )

        sun_x = 655 + math.sin(self.time * 0.12) * 12
        sun_y = 450 + math.cos(self.time * 0.09) * 5
        arcade.draw_circle_filled(sun_x, sun_y, 54, (*theme["sun"], 28))
        arcade.draw_circle_filled(sun_x, sun_y, 34, (*theme["sun"], 72))

        self.draw_stars(theme, level_number)
        self.draw_clouds(theme, level_number)
        self.draw_mountains(theme, level_number)
        self.draw_arches(theme, level_number)

        # A translucent-looking mist band separates the background from the
        # play space and gives the screen more depth.
        arcade.draw_lbwh_rectangle_filled(
            0,
            102,
            SCREEN_WIDTH,
            24,
            (*theme["mist"], 32),
        )

    def draw_stars(self, theme, level_number):
        """Draw deterministic stars that shift slightly between levels."""
        for index in range(18):
            x = (index * 137 + level_number * 41) % SCREEN_WIDTH
            y = 300 + ((index * 83 + level_number * 29) % 260)
            twinkle = 1 if (index + int(self.time * 2)) % 4 == 0 else 0
            radius = 1.5 if twinkle else 1
            arcade.draw_circle_filled(x, y, radius, (*theme["accent"], 150))

    def draw_clouds(self, theme, level_number):
        """Draw slow-moving cloud clusters behind the route."""
        cloud_color = (*theme["mist"], 34)
        drift = (self.time * 5 + level_number * 27) % 980 - 90
        for x, y, scale in ((drift, 405, 1.0), (drift - 370, 330, 0.7)):
            arcade.draw_ellipse_filled(x, y, 125 * scale, 28 * scale, cloud_color)
            arcade.draw_ellipse_filled(
                x - 32 * scale,
                y + 8 * scale,
                64 * scale,
                34 * scale,
                cloud_color,
            )
            arcade.draw_ellipse_filled(
                x + 34 * scale,
                y + 6 * scale,
                78 * scale,
                38 * scale,
                cloud_color,
            )

    def draw_mountains(self, theme, level_number):
        """Draw two parallax mountain silhouettes."""
        far_shift = (self.time * 4 + level_number * 19) % 160
        far_points = [(-160 + far_shift, 90), (0 + far_shift, 270)]
        for peak_x, peak_y in ((170, 290), (410, 250), (680, 300)):
            far_points.extend(
                [(peak_x - 150 + far_shift, 90), (peak_x + far_shift, peak_y)]
            )
        far_points.extend([(960 + far_shift, 90), (-160 + far_shift, 90)])
        arcade.draw_polygon_filled(far_points, theme["far"])

        near_shift = (self.time * 8 + level_number * 31) % 220
        near_points = [(-220 + near_shift, 50)]
        for peak_x, peak_y in ((100, 210), (350, 155), (610, 220), (850, 165)):
            near_points.extend(
                [(peak_x - 120 + near_shift, 50), (peak_x + near_shift, peak_y)]
            )
        near_points.extend([(1020 + near_shift, 50), (-220 + near_shift, 50)])
        arcade.draw_polygon_filled(near_points, theme["near"])

    def draw_arches(self, theme, level_number):
        """Add faint architectural shapes to support the climbing theme."""
        arch_color = (*theme["accent"], 24)
        spacing = 148
        shift = (level_number * 23) % spacing
        for x in range(-spacing, SCREEN_WIDTH + spacing, spacing):
            left = x + shift
            arcade.draw_lbwh_rectangle_filled(left, 0, 42, 215, arch_color)
            arcade.draw_circle_filled(left + 21, 215, 21, arch_color)


class StructureRenderer:
    """Draw the continuous tower shell surrounding every level."""

    SHELL_BODY = (22, 31, 50)
    SHELL_EDGE = (66, 88, 108)
    SHELL_INSET = (12, 20, 37)
    SHELL_JOINT = (10, 16, 30)
    SHELL_ACCENT = (118, 190, 166)
    SHELL_GOLD = (231, 179, 87)

    def draw(self, level_number):
        """Draw matching side structures that continue across all levels."""
        self.draw_side_buttress(left=True)
        self.draw_side_buttress(left=False)
        self.draw_floor_joints()
        self.draw_vertical_cables(level_number)

    def draw_side_buttress(self, left):
        """Draw one heavy side column with a consistent silhouette."""
        if left:
            polygon = [
                (0, 0),
                (0, SCREEN_HEIGHT),
                (51, SCREEN_HEIGHT),
                (67, SCREEN_HEIGHT - 18),
                (67, 18),
                (51, 0),
            ]
            inset_x = 26
            rail_x = 48
        else:
            polygon = [
                (SCREEN_WIDTH, 0),
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                (SCREEN_WIDTH - 51, SCREEN_HEIGHT),
                (SCREEN_WIDTH - 67, SCREEN_HEIGHT - 18),
                (SCREEN_WIDTH - 67, 18),
                (SCREEN_WIDTH - 51, 0),
            ]
            inset_x = SCREEN_WIDTH - 26
            rail_x = SCREEN_WIDTH - 48

        arcade.draw_polygon_filled(polygon, self.SHELL_BODY)
        arcade.draw_polygon_outline(polygon, self.SHELL_EDGE, 2)

        inset_left = inset_x - 5 if left else inset_x - 5
        arcade.draw_lbwh_rectangle_filled(
            inset_left,
            0,
            10,
            SCREEN_HEIGHT,
            self.SHELL_INSET,
        )
        arcade.draw_line(
            rail_x,
            0,
            rail_x,
            SCREEN_HEIGHT,
            self.SHELL_EDGE,
            2,
        )

        for joint_y in (75, 225, 375, 525):
            if left:
                joint_left = 6
            else:
                joint_left = SCREEN_WIDTH - 58
            arcade.draw_lbwh_rectangle_filled(
                joint_left,
                joint_y,
                52,
                5,
                self.SHELL_JOINT,
            )
            arcade.draw_line(
                joint_left + 7,
                joint_y + 4,
                joint_left + 45,
                joint_y + 4,
                self.SHELL_EDGE,
                1,
            )

    def draw_floor_joints(self):
        """Add aligned seams where one vertical level meets the next."""
        for y in (0, SCREEN_HEIGHT - 8):
            arcade.draw_lbwh_rectangle_filled(
                0,
                y,
                70,
                8,
                self.SHELL_JOINT,
            )
            arcade.draw_lbwh_rectangle_filled(
                SCREEN_WIDTH - 70,
                y,
                70,
                8,
                self.SHELL_JOINT,
            )
            arcade.draw_line(8, y + 6, 62, y + 6, self.SHELL_ACCENT, 1)
            arcade.draw_line(
                SCREEN_WIDTH - 62,
                y + 6,
                SCREEN_WIDTH - 8,
                y + 6,
                self.SHELL_ACCENT,
                1,
            )

    def draw_vertical_cables(self, level_number):
        """Draw continuous cables with a small level-based signal pulse."""
        pulse_y = 40 + ((level_number * 97) % 500)
        for x in (34, SCREEN_WIDTH - 34):
            arcade.draw_line(x, 10, x, SCREEN_HEIGHT - 10, self.SHELL_EDGE, 1)
            arcade.draw_circle_filled(x, pulse_y, 3, self.SHELL_GOLD)
            arcade.draw_circle_filled(x, pulse_y, 1.2, self.SHELL_ACCENT)


class Particle:
    """A tiny short-lived particle used for movement feedback."""

    def __init__(self, x, y, velocity_x, velocity_y, life, size, color):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life = life
        self.max_life = life
        self.size = size
        self.color = color

    def update(self, delta_time):
        """Move the particle and return whether it is still alive."""
        self.life -= delta_time
        self.x += self.velocity_x * delta_time * 60
        self.y += self.velocity_y * delta_time * 60
        self.velocity_y -= 0.08 * delta_time * 60
        return self.life > 0

    def draw(self):
        """Draw the particle with a fading alpha value."""
        alpha = int(255 * max(0, self.life / self.max_life))
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.size,
            (*self.color, alpha),
        )


class ParticleSystem:
    """Manage small bursts created by jumps, landings, and slides."""

    def __init__(self):
        self.particles = []
        self.enabled = True

    def clear(self):
        """Remove particles when a new level is loaded."""
        self.particles.clear()

    def update(self, delta_time):
        """Update all active particles."""
        self.particles = [
            particle
            for particle in self.particles
            if particle.update(delta_time)
        ]

    def draw(self):
        """Draw all active particles."""
        for particle in self.particles:
            particle.draw()

    def emit_jump(self, x, y):
        """Emit a small burst below the player when a jump begins."""
        if not self.enabled:
            return
        for index in range(5):
            direction = -1 if index % 2 else 1
            self.particles.append(
                Particle(
                    x + (index - 2) * 2,
                    y - 8,
                    direction * (0.3 + index * 0.08),
                    -0.5 - index * 0.08,
                    0.25 + index * 0.03,
                    1.5,
                    (255, 226, 145),
                )
            )

    def emit_landing(self, x, y, impact_speed):
        """Emit dust outward from a landing, scaled by impact speed."""
        if not self.enabled:
            return
        count = min(10, 4 + int(abs(impact_speed) / 2))
        for index in range(count):
            direction = -1 if index % 2 else 1
            self.particles.append(
                Particle(
                    x + direction * (index % 3),
                    y + 1,
                    direction * (1.0 + (index % 4) * 0.35),
                    0.5 + (index % 3) * 0.2,
                    0.35 + (index % 4) * 0.04,
                    1.2 + (index % 2),
                    (242, 210, 162),
                )
            )

    def emit_slide(self, x, y, direction):
        """Emit a short trail while the player is actively sliding."""
        if not self.enabled:
            return
        self.particles.append(
            Particle(
                x - direction * 5,
                y,
                -direction * 0.35,
                0.4,
                0.22,
                1.3,
                (255, 238, 173),
            )
        )
