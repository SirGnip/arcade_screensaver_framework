import time
import arcade
from arcade_screensaver_framework import screensaver_framework


class MinimalSaver(arcade.Window):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        left, self.screen_width, bottom, self.screen_height = self.get_viewport()
        self.x = 0
        self.xvel = 15

    def update(self, delta):
        self.x += self.xvel
        if self.x < 0 or self.x > self.screen_width:
            self.xvel *= -1
        time.sleep(0.03)

    def on_draw(self):
        arcade.start_render()
        ctr_x = self.screen_width // 2
        ctr_y = self.screen_height // 2

        arcade.draw_rectangle_outline(self.x, ctr_y, 200, 200, arcade.color.DARK_RASPBERRY, border_width=15)
        arcade.draw_text("Minimal Screen Saver",
                         ctr_x, ctr_y,
                         arcade.color.WHITE, 36, anchor_x="center")


if __name__ == "__main__":
    screensaver_framework.main(MinimalSaver)
