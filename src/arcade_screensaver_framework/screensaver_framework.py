import sys
import ctypes
from pathlib import Path
import pyglet
import arcade

SCREEN_WIDTH = 1280  # 720p resolution
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Arcade screen saver"
all_windows = []


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


def close_all():
    for win in all_windows:
        print("closing", win)
        win.close()


def get_preferred_screen(screens):
    """Choose the screen with the most pixels to show the screensaver on"""
    ordered_screens = [(s.width*s.height, idx, s) for idx, s in enumerate(screens)]
    ordered_screens.sort()  # sort by # of pixels, then screen index, then object
    return ordered_screens[-1][2]  # return screen object from end of sorted list


def make_windows(window_factory, is_fullscreen):
    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    preferred_screen = get_preferred_screen(screens)
    for screen in screens:
        print(screen)
        if screen == preferred_screen:
            win = window_factory(fullscreen=is_fullscreen, screen=screen)
            if not is_fullscreen:
                win.set_location(screen.x + 50, screen.y + 50)
            all_windows.append(win)
        else:
            pyglet_win = pyglet.window.Window(fullscreen=is_fullscreen, screen=screen)
            pyglet_win.on_close = close_all
            if not is_fullscreen:
                pyglet_win.set_location(screen.x + 50, screen.y + 50)
            all_windows.append(pyglet_win)


def main(window_factory):
    # Screen saver command line arguments: https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    print("Command line args:", sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1].startswith("/p"):
        # mini-screen preview of screen saver
        print("screen saver launch preview", sys.argv)
    elif len(sys.argv) >= 2 and sys.argv[1].startswith("/c"):
        # settings dialog box
        name = Path(sys.argv[0]).stem
        MB_ICONINFORMATION = 0x00000040
        ctypes.windll.user32.MessageBoxW(0, f"This screen saver has no options that you can set.", f"{name} Screen Saver", MB_ICONINFORMATION)
    elif len(sys.argv) >= 2 and sys.argv[1] == "/s":
        # run screen saver (in fullscreen mode)
        print("screen saver fullscreen", sys.argv)
        make_windows(window_factory, True)
        arcade.run()
    else:
        # launch with no arguments to test screen saver in windowed mode
        print("screen saver windowed test mode")
        make_windows(window_factory, False)
        arcade.run()
