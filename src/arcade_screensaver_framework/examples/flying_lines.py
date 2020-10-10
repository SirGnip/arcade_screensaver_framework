from typing import Dict
import random
import time
from dataclasses import dataclass
import arcade
from arcade_screensaver_framework import screensaver_framework

LINE_WIDTH = 8

COLORS_GREENS = (
        (1, 25, 16),
        (
            arcade.color.WHITE,
            arcade.color.LIGHT_GREEN,
            arcade.color.LIGHT_GREEN,
            arcade.color.GREEN,
            arcade.color.GREEN,
            arcade.color.DARK_GREEN,
        )
    )

COLORS_RED_BLUE = (
        (0x02, 0x05, 0x14),
        (
            (0x0F, 0x25, 0xA2),
            (0x0F, 0x25, 0xA2),
            (0x0F, 0x25, 0xA2),
            (0x0F, 0x25, 0xA2),
            (0xDB, 0x00, 0x00),
            (0xDB, 0x00, 0x00),
            (0xDB, 0x00, 0x00),
            (0xDB, 0x00, 0x00),
            (0xF7, 0xD4, 0x51),
        )
    )

COLORS = random.choice((COLORS_GREENS, COLORS_RED_BLUE))


@dataclass
class Line:
    x: float
    y: float
    length: float
    x_vel: float
    color: arcade.Color

    @staticmethod
    def factory(mid_y, sigma):
        length = random.randint(75, 400)
        start_x = 0 - length - 5  # make sure new Lines start off screen
        y = random.normalvariate(mid_y, sigma)
        if y > mid_y:
            # spread out distribution of values above the mean line
            y = ((y - mid_y) * 4.0) + mid_y

        return Line(
            start_x,
            y,
            length,
            random.uniform(3, 9),
            random.choice(COLORS[1])
        )

    def randomize_x(self, screen_width):
        self.x = random.randint(0, screen_width)
        return self

    def move(self):
        self.x += self.x_vel

    def can_reap(self, screen_width):
        return self.x > screen_width


class FlyingLinesScreensaver(arcade.Window):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        arcade.set_background_color(COLORS[0])

        left, self.screen_width, bottom, self.screen_height = self.get_viewport()
        print(f"screen width/height={self.screen_width}/{self.screen_height}")
        # Scale values for different size screens
        self.line_count = int((self.screen_height + self.screen_width)* 0.092)  # baseline: count=400 at 3072x1280
        self.mid_y = int(self.screen_height * 0.33)
        self.sigma = self.screen_height * 0.0469  # baseline: sigma=60 at height of 1280
        print(f"line_count={self.line_count} mid_y={self.mid_y} sigma={self.sigma}")

        # create initial lines with starting position
        self.lines = [Line.factory(self.mid_y, self.sigma).randomize_x(self.screen_width) for _ in range(self.line_count)]

    def update(self, dt):
        time.sleep(0.025)

        for line in self.lines:
            line.move()

        # remove lines that can be reaped
        self.lines = [line for line in self.lines if not line.can_reap(self.screen_width)]

        # create new lines
        while len(self.lines) < self.line_count:
            self.lines.append(Line.factory(self.mid_y, self.sigma))

    def on_draw(self):
        arcade.start_render()
        points_per_color: Dict[arcade.Color, arcade.PointList] = {}
        for l in self.lines:
            color_specific_point_list = points_per_color.setdefault(l.color, [])
            color_specific_point_list.append((l.x, l.y))
            color_specific_point_list.append((l.x + l.length, l.y))
        # Need to sort by key so the colors are always drawn in a stable order.
        # Without sorting, the draw order of the colors would pop occasionally
        # because dicts do not preserve key ordering.
        for color in sorted(points_per_color.keys()):
            # draw_lines() is much faster than draw_line()
            arcade.draw_lines(points_per_color[color], color, LINE_WIDTH)


if __name__ == "__main__":
    screensaver_framework.create_screensaver_window(FlyingLinesScreensaver)
    arcade.run()
