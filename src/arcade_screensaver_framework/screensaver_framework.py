import sys
import ctypes
from pathlib import Path
import pyglet
import arcade

SCREEN_WIDTH = 1280  # 720p resolution
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Arcade screen saver"
all_windows = []


# Event handlers that can be applied to instances of Arcade.Window and Pyglet.window.Window
def on_keyboard_press(self, symbol, modifiers):
    close_all_windows()


def on_mouse_press(self, x, y, button, modifiers):
    close_all_windows()


def on_mouse_motion(self, x, y, dx, dy):
    # A Window almost always gets an initial on_mouse_motion event when window opens.
    # Ignore the first motion event. I think a motion event is triggered when the
    # window is opening and the mouse cursor is already inside the window's boundary.
    if self.first_mouse_motion_event:
        self.first_mouse_motion_event = False
        return
    close_all_windows()


def on_close(self):
    close_all_windows()


def close_all_windows():
    for win in all_windows:
        win.close()


def get_preferred_screen(screens):
    """Choose the screen with the most pixels to show the screensaver on"""
    ordered_screens = [(s.width*s.height, idx, s) for idx, s in enumerate(screens)]
    ordered_screens.sort()  # sort by # of pixels, then screen index, then object
    return ordered_screens[-1][2]  # return screen object from end of sorted list


def make_windows(screensaver_window_class, is_fullscreen):
    # Monkeypatch Arcade and Pyglet window classes (for easier code-reuse)
    screensaver_window_class.on_key_press = on_keyboard_press
    screensaver_window_class.on_mouse_press = on_mouse_press
    screensaver_window_class.on_mouse_motion = on_mouse_motion
    screensaver_window_class.on_close = on_close

    pyglet.window.Window.on_key_press = on_keyboard_press
    pyglet.window.Window.on_mouse_press = on_mouse_press
    pyglet.window.Window.on_mouse_motion = on_mouse_motion
    pyglet.window.Window.on_close = on_close

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    preferred_screen = get_preferred_screen(screens)
    for screen in screens:
        if screen == preferred_screen:
            # Arcade managed screen with screen saver on it
            win = screensaver_window_class(fullscreen=is_fullscreen, screen=screen)
        else:
            # Pyglet managed screen that is simply left clear
            win = pyglet.window.Window(fullscreen=is_fullscreen, screen=screen)
        win.set_mouse_visible(False)
        win.first_mouse_motion_event = True
        if not is_fullscreen:
            win.set_location(screen.x + 50, screen.y + 50)
        all_windows.append(win)


def main(screensaver_window_class):
    # Screen saver command line arguments: https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    if len(sys.argv) >= 2 and sys.argv[1].startswith("/p"):
        # generate mini-screen preview for screen saver
        pass  # skip preview
    elif len(sys.argv) >= 2 and sys.argv[1].startswith("/c"):
        # settings dialog box
        name = Path(sys.argv[0]).stem
        MB_ICONINFORMATION = 0x00000040
        ctypes.windll.user32.MessageBoxW(0, f"This screen saver has no options that you can set.", f"{name} Screen Saver", MB_ICONINFORMATION)
    elif len(sys.argv) >= 2 and sys.argv[1] == "/s":
        # run screen saver in fullscreen mode
        make_windows(screensaver_window_class, True)
        arcade.run()
    else:
        # launch with no arguments to test screen saver in windowed mode
        make_windows(screensaver_window_class, False)
        arcade.run()
