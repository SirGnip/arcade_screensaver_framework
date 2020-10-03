import time
import random
from typing import Generator
from dataclasses import dataclass, field
import arcade
from gnp.arcadelib.actor import Actor, ActorList
from gnp.arcadelib import scriptutl
from arcade_screensaver_framework import screensaver_framework


@dataclass
class Arc(Actor):
    x: float
    y: float
    radius: float
    color: arcade.Color
    start_angle: float
    end_angle: float
    line_width: float
    rotation: float
    rotation_velocity: float
    anim_script: Generator[None, None, None] = field(init=False)

    def __post_init__(self):
        self.anim_script = self.script()

    def update(self, delta_time: float):
        if self.anim_script:
            try:
                next(self.anim_script)
            except StopIteration:
                pass
        self.rotation += self.rotation_velocity

    def draw(self):
        arcade.draw_arc_outline(self.x, self.y, self.radius * 2, self.radius * 2, self.color, self.start_angle, self.end_angle, self.line_width, self.rotation)

    def script(self):
        """Generator based 'script' to drive animation"""
        while True:
            self.rotation_velocity = 0.0
            yield from scriptutl.sleep(random.uniform(1.0, 30.0))
            self.rotation_velocity = random.choice((-1.0, 1.0))
            yield from scriptutl.sleep(random.uniform(1.0, 5.0))

    def can_reap(self):
        return False


@dataclass
class Coil(Actor):
    x: float
    y: float
    start_radius: float
    radius_step: float
    arc_count: int
    arcs: ActorList = None

    def __post_init__(self):
        LINE_WIDTH = 20
        ALPHA = 200
        self.arcs = ActorList()
        radii = [r*self.radius_step+self.start_radius for r in range(self.arc_count)]
        for idx, radius in enumerate(radii):
            angle_start = random.choice((0, 90, 180, 270))
            angle_size = random.choice((90, 180, 270))
            angle_end = angle_start + angle_size
            color = arcade.color.MIDNIGHT_BLUE + (ALPHA,) if idx % 2 == 0 else arcade.color.DARK_BLUE_GRAY + (ALPHA,)
            arc = Arc(self.x, self.y, radius, color, angle_start, angle_end, LINE_WIDTH, 0, 0.0)
            self.arcs.append(arc)

    def update(self, delta_time: float):
        self.arcs.update(delta_time)

    def draw(self):
        self.arcs.draw()

    def can_reap(self):
        return False


class RotatingArcsSaver(arcade.Window):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        left, self.screen_width, bottom, self.screen_height = self.get_viewport()
        # self.tilt = 0

        self.coils = ActorList()
        for _ in range(20):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            arc_count = random.randint(3, 7)
            self.coils.append(Coil(x, y, 25, 25, arc_count))

        # LINE_WIDTH = 20
        # x = self.screen_width // 2
        # y = self.screen_height // 2
        # self.arcs = ActorList()
        # for radius in range(25, 400, 25):
        # for radius in (100,):
        #     angle_start = random.choice((0, 90, 180, 270))
        #     angle_size = random.choice((90, 180, 270))
        #     angle_end = angle_start + angle_size
        #     rot_vel = random.choice((-2, -1, -0.5, 0, 0, 0, 0.5, 1, 2))
        #     arc = Arc(x, y, radius, arcade.color.MIDNIGHT_BLUE, angle_start, angle_end, LINE_WIDTH, 0, rot_vel)
        #     self.arcs.append(arc)

    def update(self, delta):
        time.sleep(0.03)
        # self.arcs.update(delta)
        self.coils.update(delta)

    def on_draw(self):
        arcade.start_render()
        # self.arcs.draw()
        self.coils.draw()

        # width = 15
        # arcade.draw_arc_outline(200, 200, 175, 175, arcade.color.MIDNIGHT_BLUE, 0, 270, width, self.tilt * 2)
        # arcade.draw_arc_outline(200, 200, 125, 125, arcade.color.MIDNIGHT_BLUE, 0, 90, width, self.tilt * 2)
        # arcade.draw_arc_outline(200, 200, 100, 100, arcade.color.MIDNIGHT_BLUE, 0, 270, width, self.tilt)
        # arcade.draw_arc_outline(200, 200, 75, 75, arcade.color.MIDNIGHT_BLUE, 0, 180, width, -self.tilt)


if __name__ == "__main__":
    screensaver_framework.main(RotatingArcsSaver)
