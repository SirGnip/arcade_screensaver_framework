import random
import time
import arcade
from arcade_screensaver_framework import screensaver_framework
from gnp.arcadelib.actor import Actor, ActorList
from gnp.arcadelib import scriptutl


class RingActor(Actor):
    def __init__(self, x, y, radius_vel, color):
        self.x = x
        self.y = y
        self.radius_vel = radius_vel
        self.color = color
        self.radius = 5.0
        self.lifetime_start = 0.7
        self.lifetime = self.lifetime_start

    def update(self, delta_time: float):
        self.lifetime -= 1/60.0
        self.radius += self.radius_vel

    def draw(self):
        alpha = 255 * (self.lifetime / self.lifetime_start)
        arcade.draw_circle_outline(self.x, self.y, self.radius, self.color + (alpha,), 10)

    def can_reap(self) -> bool:
        """Allows an Actor to manage its own lifetime"""
        return self.lifetime < 0.0


class RingActorLeader(RingActor):
    """The first raindrop tha spawns other rings"""
    def __init__(self, actor_list, x, y, radius_vel, color):
        super().__init__(x, y, radius_vel, color)
        self.actor_list = actor_list
        self.script = self.script()

    def script(self):
        """Generator used for cooperative multitasking"""
        # sleep and then spawn a new ring a few times
        j = 1.0
        jv = 0.15
        for _ in range(4):
            yield from scriptutl.sleep(0.17)
            jitx = random.uniform(-j, j)
            jity = random.uniform(-j, j)
            jitvel = random.uniform(-jv, jv)
            self.actor_list.append(RingActor(self.x + jitx, self.y + jity, self.radius_vel + jitvel, self.color))

    def update(self, delta_time: float):
        super().update(delta_time)
        try:
            next(self.script)
        except StopIteration:
            pass


class RaindropScreensaver(arcade.Window):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        arcade.set_background_color(arcade.color.BLACK)

        left, self.screen_width, bottom, self.screen_height = self.get_viewport()
        print(f"screen width/height={self.screen_width}/{self.screen_height}")
        self.actors = ActorList()

    def update(self, delta_time: float):
        time.sleep(0.025)
        if random.randint(1, 4) == 1:
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            self.actors.append(RingActorLeader(self.actors, x, y, 6.0, arcade.color.BLUE_VIOLET))
        self.actors.update(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.actors.draw()


if __name__ == "__main__":
    screensaver_framework.main(RaindropScreensaver)
