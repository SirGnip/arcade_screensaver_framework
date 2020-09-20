import random
import time
from dataclasses import dataclass
import arcade
from arcade_screensaver_framework import screensaver_framework

LINE_COUNT = 300

@dataclass
class Line:
    x: float
    y: float
    len: float
    x_vel: float
    color: arcade.Color

    @staticmethod
    def factory(mid_y):
        length = random.randint(75, 400)
        start_x = 0 - length - 5  # make sure new Lines start off screen
        # y = random.randint(mid_y - 200, mid_y + 200) # uniform distribution
        y = random.normalvariate(mid_y, 60)
        if y > mid_y:
            # spread out distribution of values above the mean line
            y = ((y - mid_y) * 4.0) + mid_y

        return Line(
            start_x,
            y,
            length,
            random.uniform(3, 9),
            random.choice((
                arcade.color.WHITE,
                arcade.color.LIGHT_GREEN,
                arcade.color.LIGHT_GREEN,
                arcade.color.GREEN,
                arcade.color.GREEN,
                arcade.color.DARK_GREEN,
            ))
        )

    def randomize_x(self, screen_width):
        self.x = random.randint(0, screen_width)
        return self

    def move(self):
        self.x += self.x_vel

    def draw(self):
        arcade.draw_line(self.x, self.y, self.x + self.len, self.y, self.color, 5)

    def can_reap(self, screen_width):
        return self.x > screen_width


class FlyingLinesScreensaver(screensaver_framework.ScreenSaverWindow):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen, screen)
        left, self.screen_width, bottom, self.screen_height = self.get_viewport()
        self.mid_y = int(self.screen_height * 0.33)
        # self.mid_y = self.screen_height // 2
        arcade.set_background_color((1, 25, 16))  # a darker DARK_GREEN

        # starting lines
        self.lines = [Line.factory(self.mid_y).randomize_x(self.screen_width) for _ in range(LINE_COUNT)]

    def update(self, dt):
        for line in self.lines:
            line.move()

        # remove lines that can be reaped
        self.lines = [line for line in self.lines if not line.can_reap(self.screen_width)]

        # create new lines
        while len(self.lines) < LINE_COUNT:
            self.lines.append(Line.factory(self.mid_y))

    def on_draw(self):
        arcade.start_render()
        for line in self.lines:
            line.draw()


if __name__ == "__main__":
    screensaver_framework.main(FlyingLinesScreensaver)
