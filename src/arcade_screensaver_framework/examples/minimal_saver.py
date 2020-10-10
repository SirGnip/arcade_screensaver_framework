import arcade
from arcade_screensaver_framework import screensaver_framework


class MinimalSaver(arcade.Window):
    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        self.x = 0

    def on_draw(self):
        self.x = (self.x + 10) % self.get_size()[0]
        arcade.start_render()
        arcade.draw_rectangle_filled(self.x, self.get_size()[1] / 2, 200, 200, arcade.color.BLUE)


if __name__ == "__main__":
    window = screensaver_framework.create_screensaver_window(MinimalSaver)
    arcade.run()
