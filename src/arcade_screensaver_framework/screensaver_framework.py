import sys
import pyglet
import arcade

SCREEN_WIDTH = 1280  # 720p resolution
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Arcade screen saver"


class ScreenSaverWindow(arcade.Window):
    """Base class for all screen saver windows"""
    def __init__(self, fullscreen, screen):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=fullscreen, screen=screen)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print('on mouse press')
        close_all()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass
        # print("on mouse motion", x, y, dx, dy)
        # window always gets an initial mouse motion event?

    def on_key_press(self, key, modifiers):
        print("on key press")
        close_all()


all_windows = []


def close_all():
    for win in all_windows:
        print("closing", win)
        win.close()


def main(window_factory):
    print("Command line args:", sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == "/p":
        print("screen saver preview", sys.argv)
    elif len(sys.argv) >= 2 and sys.argv[1] == "/c":
        print("screen saver config", sys.argv)
    elif len(sys.argv) >= 2 and sys.argv[1] == "/s":
        print("screen saver fullscreen", sys.argv)
        display = pyglet.canvas.get_display()
        screens = display.get_screens()
        for s in screens:
            print(s)

        win1 = window_factory(fullscreen=True, screen=screens[0])
        all_windows.append(win1)

        pyglet_win = pyglet.window.Window(fullscreen=True, screen=screens[1])
        pyglet_win.on_close = close_all
        all_windows.append(pyglet_win)

        arcade.run()  # similar to pyglet.app.run

    else:
        print("screen saver windowed test mode")
        display = pyglet.canvas.get_display()
        screens = display.get_screens()
        for s in screens:
            print(s)

        win1 = window_factory(fullscreen=False, screen=screens[0])
        win1.set_location(screens[0].x+50, screens[0].y+50)
        all_windows.append(win1)

        pyglet_win = pyglet.window.Window(fullscreen=False, screen=screens[1])
        pyglet_win.on_close = close_all
        pyglet_win.set_location(screens[1].x+50, screens[1].y+50)
        all_windows.append(pyglet_win)

        arcade.run()  # similar to pyglet.app.run



