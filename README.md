# Arcade Screen Saver Framework

A very simple Python framework that allows you to write official Windows screen savers using
Python and the [Arcade](https://github.com/pythonarcade/arcade) 2D video game library.

Most Arcade scripts that use the class-centric Arcade API (ex: derive a window from `arcade.Window`)
can easily be made into a Windows screen saver with this framework. Often, it is as simple as adding the
framework import to an existing Arcade script and creating your window object with `window = screensaver_framework.create_saver_win(MyGameClass)`

### Examples

A few simple examples are included along with the framework. Flying Lines, Raindrops, and Ovals:

![Flying Lines](https://sirgnip.github.io/repo/arcade_screensaver_framework/flying_lines_30fps_40pct.gif)
![Raindrops](https://sirgnip.github.io/repo/arcade_screensaver_framework/raindrops_30fps_40pct.gif)
![Ovals](https://sirgnip.github.io/repo/arcade_screensaver_framework/ovals_30fps_40pct.gif)

### Features
 
This framework provides your script:
* What it needs to interface with Windows so your Arcade application is seen as an official Windows screen saver.
* Input event handling to automatically close the script when any keyboard or mouse input is detected.
* Handling of multi-monitor setups (draws screen saver visuals on largest monitor and shows black screen on the others)
* An included installation script that takes your Arcade application and:
    * Bundles your script and its dependencies into a one-file .exe (via PyInstaller) necessary for Windows screen savers
    * Copies the bundled executable into the appropriate with the appropriate name so that Windows recognizes it as a screen saver.

# Quick start

Install framework:

    pip install git+https://github.com/SirGnip/arcade_screensaver_framework

Manually run screen saver examples (`/s` runs app in fullscreen)

    python -m arcade_screensaver_framework.examples.minimal_saver /s
    python -m arcade_screensaver_framework.examples.flying_lines /s
    python -m arcade_screensaver_framework.examples.oval_screensaver /s
    python -m arcade_screensaver_framework.examples.raindrops /s

Install one of the included example screen savers as a fully functional Windows screen saver.
Run the command below from a Command Prompt. This Command Prompt **MUST** be run with "Run as administrator". Make
sure the Python environment that you installed the framework to is active.
    
    # The example scripts are often located in a path similar to the following.
    # Your actual path may vary...
    
    install_screensaver venv\Lib\site-packages\arcade_screensaver_framework\examples\minimal_saver.py

After installation, you need to go into Window's "Screen Saver Settings" dialog and
select your newly installed screen saver.  This is usually accomplished by following steps similar to:

* Right click on the Windows desktop
* Select "Personalize"
* Click "Lock screen" in the left pane
* Scroll to the bottom of the dialog and click the link labeled "Screen saver settings"
* In the "Screen Saver Settings" dialog, select your newly installed screen saver from the dropdown
* Enter a "Wait" time for how long your computer must be idle before it displays the screen saver
* Click the "Preview" button to see your screen saver 

*Note: The "Screen Saver Settings" dialog will feel very sluggish while your have a custom
screen saver selected. This is because Windows is running the screen saver application
in the background as you click through the options in the dialog. Each run of the
application takes a couple seconds to complete. This is because of how PyInstaller bundles Python scripts.*

# Write your own screen saver

## Quick demonstration

Install framework:

    pip install git+https://github.com/SirGnip/arcade_screensaver_framework

Save the following script as "my_test.py"

    import arcade
    from arcade_screensaver_framework import screensaver_framework
    
    class MinimalSaver(arcade.Window):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.x = 0
    
        def on_draw(self):
            self.x = (self.x + 10) % self.get_size()[0]
            arcade.start_render()
            arcade.draw_rectangle_filled(self.x, self.get_size()[1] / 2, 200, 200, arcade.color.BLUE)

    if __name__ == "__main__":
        screensaver_framework.create_screensaver_window(MinimalSaver)
        arcade.run()

Run script manually to test (notice how it exits when you cause any input events):

    python my_test.py /s
    
Open a Command Prompt terminal with "Run as administrator", change directory to where your `my_test.py` script is, active your Python environment, and then run:

    install_screensaver my_test.py

As the `arcade_screensaver_framework` handles input events for you, your code doesn't need any `on_keyboard_press`, `on_mouse_press`, `on_mouse_motion` event handlers.

## Steps required

To write an Arcade script that can be used as a screen saver, just a few things need to be done in the code.
Refer to the `my_test.py` example above for a concrete illustration of the points below.

First, import the module at the top of your script:

    from arcade_screensaver_framework import screensaver_framework
    
Second, the window class for your app must derive from `arcade.Window`:

    class MyWindow(arcade.Window):

Third, write an `__init__` method for the `Window` class that accepts `*args` and `**kwargs`
and pass them to the `super()` class. This is required to allow the `arcade_screensaver_framework`
to pass a couple arguments into the `__init__` method: 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = 0

Fourth, instead of creating the Arcade window with the typical `win = MyWindow()`, you need to
use the `arcade_screensaver_framework` to create the window for you:

    win = screensaver_framework.create_screensaver_window(MyWindow)
    arcade.run()

## Implementation details

### Listing this framework as a dependency

To include this library in a `requirements.txt` file, use this syntax:

    git+https://github.com/SirGnip/arcade_screensaver_framework@v0.0.1

To include this library in a setup.py file, use syntax something like this:

    install_requires=[
        "arcade_screensaver_framework @ http://github.com/SirGnip/arcade_screensaver_framework/tarball/v0.0.1",
    ],

### Input events

The framework handles closing the application when receiving input. So, do not
try to provide input event handlers like `on_mouse_motion` or `on_keyboard_press`
as these could interfere with arcade_screensaver_framework's operation.

### Resolution selection

When the screen saver is run in fullscreen mode, the framework chooses the most
appropriate screen resolution. This way, your application can run on computers
with screens of any size. This means your screen saver should query the size of
the screen when it starts with a function like `.get_size()` and adjust to the
height and width dynamically.

### Parameters for `create_screensaver_window()`

    create_screensaver_window(WINDOW_CLASS, **kwargs)
    
- first parameter: the class of the Window that runs your screen saver 
- second parameter (optional): can specify keyword arguments that will be passed to the
`Windows` constructor

### Requirements for an application to function as a Windows screen saver

For an application to be an official Windows screen saver, it must do the following things:

| Requirements | How this framework fulfills requirement |
|--------------|-----------------------------------------|
| Must be a Windows .exe file. | The `install_screensaver.bat` script uses [PyInstaller](https://www.pyinstaller.org/) to bundle the Python script into an .exe. |
| The .exe must be renamed to have a `.scr` extension and be saved into a specific Windows system directory. | Handled by `install_screensaver.bat` script. | 
| Must handle a few command line flags when run. This is how Windows controls the screen saver. | This framework parses the command line flags and responds appropriately. |  
| Executable must exit when it receives keyboard or mouse input events. | Input handling is taken care of by the framework. |

Reference: Windows [Screen Saver command line arguments](https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line)

![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2FSirGnip%2Farcade_screensaver_framework)

![HitCount](http://hits.dwyl.com/SirGnip/arcade_screensaver_framework.svg)
