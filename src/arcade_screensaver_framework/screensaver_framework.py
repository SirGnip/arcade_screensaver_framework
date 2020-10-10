import sys
import ctypes
from pathlib import Path
import pyglet

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


def _make_windows(screensaver_window_class, is_fullscreen, width, height, win_kwargs):
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
    main_win = None
    for screen in screens:
        if screen == preferred_screen:
            # Arcade managed screen with screen saver on it
            print("Preferred screen:", screen)
            win = screensaver_window_class(width, height, fullscreen=is_fullscreen, screen=screen, **win_kwargs)
            main_win = win
        else:
            # Blank Pyglet windows will be used for all non-primary screens
            print("Secondary screen:", screen)
            win = pyglet.window.Window(width, height, fullscreen=is_fullscreen, screen=screen)
        win.set_mouse_visible(False)
        win.first_mouse_motion_event = True
        if not is_fullscreen:
            win.set_location(screen.x + 50, screen.y + 50)
        all_windows.append(win)
    return main_win


def create_saver_win(screensaver_window_class, width, height, force_fullscreen_resolution, **win_kwargs):
    forbidden_kwargs = {"width", "height", "fullscreen", "screen"}
    invalid_kwargs = forbidden_kwargs.intersection(set(win_kwargs))
    if any(invalid_kwargs):
        raise Exception(f"Detected forbidden keyword argument(s) passed to create_saver_win() in 'win_kwargs': {invalid_kwargs}. These arguments are controlled by arcade_screensaver_framework.")

    # Microsoft Windows screen saver command line arguments: https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    if len(sys.argv) >= 2 and sys.argv[1].startswith("/p"):
        # generate mini-screen preview for screen saver
        pass  # skip preview
    elif len(sys.argv) >= 2 and sys.argv[1].startswith("/c"):
        # settings dialog box
        name = Path(sys.argv[0]).stem
        MB_ICONINFORMATION = 0x00000040
        ctypes.windll.user32.MessageBoxW(0, "This screen saver has no options that you can set.", f"{name} Screen Saver", MB_ICONINFORMATION)
    elif len(sys.argv) >= 2 and sys.argv[1] == "/s":
        # run screen saver in fullscreen mode
        main_win = _make_windows(screensaver_window_class, True, width, height, win_kwargs)
        if force_fullscreen_resolution:
            print(f"Scaling fullscreen {width}x{height} content to", main_win.screen)
            main_win.set_fullscreen(True, width=width, height=height)
        return main_win
    else:
        # run screen saver in windowed mode (no arguments)
        main_win = _make_windows(screensaver_window_class, False, width, height, win_kwargs)
        return main_win
