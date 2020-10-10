import sys
import ctypes
from pathlib import Path
import pyglet

all_windows = []


# Event handlers that can be applied to instances of Arcade.Window and Pyglet.window.Window
def _on_keyboard_press(self, symbol, modifiers):
    _close_all_windows()


def _on_mouse_press(self, x, y, button, modifiers):
    _close_all_windows()


def _on_mouse_motion(self, x, y, dx, dy):
    # A Window almost always gets an initial on_mouse_motion event when window opens.
    # Ignore the first motion event. I think a motion event is triggered when the
    # window is opening and the mouse cursor is already inside the window's boundary.
    if self.first_mouse_motion_event:
        self.first_mouse_motion_event = False
        return
    _close_all_windows()


def _on_close(self):
    _close_all_windows()


def _close_all_windows():
    for win in all_windows:
        win.close()


def _get_preferred_screen(screens):
    """Choose the screen with the most pixels to show the screensaver on"""
    ordered_screens = [(s.width*s.height, idx, s) for idx, s in enumerate(screens)]
    ordered_screens.sort()  # sort by # of pixels, then screen index, then object
    return ordered_screens[-1][2]  # return screen object from end of sorted list


def _make_windows(screensaver_window_class, is_fullscreen, win_kwargs):
    # Monkeypatch Arcade and Pyglet window classes (for easier code-reuse)
    screensaver_window_class.on_key_press = _on_keyboard_press
    screensaver_window_class.on_mouse_press = _on_mouse_press
    screensaver_window_class.on_mouse_motion = _on_mouse_motion
    screensaver_window_class.on_close = _on_close

    pyglet.window.Window.on_key_press = _on_keyboard_press
    pyglet.window.Window.on_mouse_press = _on_mouse_press
    pyglet.window.Window.on_mouse_motion = _on_mouse_motion
    pyglet.window.Window.on_close = _on_close

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    preferred_screen = _get_preferred_screen(screens)
    main_win = None
    for screen in screens:
        if screen == preferred_screen:
            # Arcade managed screen with screen saver on it
            print("Preferred screen:", screen)
            win = screensaver_window_class(fullscreen=is_fullscreen, screen=screen, **win_kwargs)
            main_win = win
        else:
            # Blank Pyglet windows will be used for all non-primary screens
            print("Secondary screen:", screen)
            win = pyglet.window.Window(fullscreen=is_fullscreen, screen=screen)
        win.set_mouse_visible(False)
        win.first_mouse_motion_event = True
        all_windows.append(win)
    return main_win


def create_screensaver_window(screensaver_window_class, **win_kwargs):
    forbidden_kwargs = {"fullscreen", "screen"}
    invalid_kwargs = forbidden_kwargs.intersection(set(win_kwargs))
    if any(invalid_kwargs):
        raise Exception(f"Detected forbidden keyword argument(s) passed to create_screensaver_window() in 'win_kwargs': {invalid_kwargs}. These arguments are controlled by arcade_screensaver_framework.")

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
        main_win = _make_windows(screensaver_window_class, True, win_kwargs)
        return main_win
    else:
        # run screen saver in windowed mode (no arguments)
        main_win = _make_windows(screensaver_window_class, False, win_kwargs)
        return main_win
