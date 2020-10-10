# Arcade Screen Saver Framework

A very simple Python framework for making screen savers for Windows.  Uses the [Arcade](https://github.com/pythonarcade/arcade) 2D video game library.

Most Arcade applications that use the class-centric Arcade API (ex: derive a window from `arcade.Window`) can be made into a Windows screen saver.
Usually, it is as simple as adding the framework import to your existing application and creating your window with `window = screensaver_framework.create_saver_win(MyGameClass)`
 
This framework provides your app:
* What it needs to interface with Windows so your Arcade application is seen as an official Windows screen saver.
* Input event handling to automatically exit the application when any keyboard or mouse input is detected.
* Handling of multi-monitor setups (draws screen saver on largest screen)
* An included installation script that takes your Arcade application and:
    * Bundles it into a one-file executable (via PyInstaller) necessary for Windows screen savers
    * Installs the bundle in the appropriate place with the appropriate name so that Windows can find it.

# Quick start

Install framework:

    pip install git+https://github.com/SirGnip/arcade_screensaver_framework

Manually run screen saver examples (`/s` runs app in fullscreen)

    python -m arcade_screensaver_framework.examples.minimal_saver /s
    python -m arcade_screensaver_framework.examples.flying_lines /s
    python -m arcade_screensaver_framework.examples.oval_screensaver /s
    python -m arcade_screensaver_framework.examples.raindrops /s

Create a fully functional Windows screen saver by installing one of the provided example screen savers.
Must run this command from a Command Prompt that was opened with "Run as administrator".
    
    # The example scripts are often located in a path similar to the following.
    # Your actual path may vary...
    
    install_screensaver venv\Lib\site-packages\arcade_screensaver_framework\examples\minimal_saver.py

After installation, you need to go into Window's "Screen Saver Settings" dialog and
select your newly installed screen saver.  Click the "Preview" button on the dialog
and you should see your screen saver appear after a couple seconds.  

*Note: The "Screen Saver Settings" dialog will feel very sluggish while your have a custom
screen saver selected. This is because Windows is running the screen saver application
in the background as you click through the options in the dialog. Each run of the
application takes a couple seconds to complete.*

# Write your own screen saver

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

Run script manually to test (notice how it exists when you cause any input events):

    python my_test.py /s
    
Open a Command Prompt terminal with "Run as administrator", make sure the proper Python environment is active and then run:

    install_screensaver my_test.py

As the `arcade_screensaver_framework` handles input events, your code shouldn't have any `on_keyboard_press`, `on_mouse_press`, `on_mouse_motion` event handlers.

# Technical reference

## What is required in a screen saver

To write an Arcade script that can be used as a screen saver, just a few things need to be done.
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
use the  `arcade_screensaver_framework` to create the window for you:

    win = screensaver_framework.create_screensaver_window(MyWindow)
    arcade.run()

## Details:

### Input Events

 The framework handles closing the application when receiving input. So, do not
try to provide input event handlers like `on_mouse_motion` or `on_keyboard_press`
as these could interfere with arcade_screensaver_framework's operation.

### Resolution selection
When the screensaver is run in fullscreen mode, the framework chooses the most
appropriate screen resolution. This way, your application can run on computers
with screens of any size. This means your screen saver should query the size of
the screen when it starts with a function like `.get_size()` and adjust to the
height and width dynamically.

### Parameters for `create_screensaver_window()`

    create_screensaver_window(WINDOW_CLASS, **kwargs)
    
- first parameter: the class of the Window that runs your screen saver 
- second parameter (optional): can specify keyword arguments that will be passed to the
`Windows` constructor

![Hits](http://cc.amazingcounters.com/counter.php?i=3245831&c=9737806)
