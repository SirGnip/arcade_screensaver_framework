import time
import random
import arcade
from arcade_screensaver_framework import screensaver_framework


class OvalShape:
    def __init__(self, x, y, width, height, angle):
        alpha = 96
        if random.choice((True, True)):
            self.color = random.choice((
                arcade.color.RED + (alpha,),
                arcade.color.BLUE + (alpha,),
                arcade.color.YELLOW + (alpha,),
            ))
        else:
            self.color = random.choice((
                arcade.color.RED + (alpha,),
                arcade.color.RED + (alpha,),
                arcade.color.RED + (alpha,),
                arcade.color.BLUE + (alpha,),
                arcade.color.BLUE + (alpha,),
                arcade.color.BLUE + (alpha,),
                arcade.color.WHITE + (alpha,),
            ))

        self.x = x
        self.y = y
        self.angle = angle
        self.delta_angle = random.uniform(0.2, 0.6)
        shape = arcade.create_ellipse_filled(0, 0, width, height, self.color, 0)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y

    def move(self):
        self.angle += self.delta_angle

    def draw(self):
        # PROBLEM: have to set center_x, etc each frame because of bug with 2.4.2
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        self.shape_list.angle = self.angle
        self.shape_list.draw()


class MyScreensaver(arcade.Window):
    """ Main application class. """

    def __init__(self, fullscreen, screen):
        super().__init__(fullscreen=fullscreen, screen=screen)
        left, self.screen_width, bottom, self.screen_height = self.get_viewport()

        self.shapes = []

        for i in range(150):
            x = random.randrange(0, self.screen_width)
            y = random.randrange(0, self.screen_height)
            width = random.randrange(75, 250)
            height = random.randrange(75, 250)
            angle = random.randrange(0, 360)

            shape = OvalShape(x, y, width, height, angle)
            self.shapes.append(shape)

    def update(self, dt):
        time.sleep(0.09)  # 10 fps
        for shape in self.shapes:
            shape.move()

    def on_draw(self):
        arcade.start_render()

        for shape in self.shapes:
            shape.draw()


if __name__ == "__main__":
    screensaver_framework.main(MyScreensaver)
