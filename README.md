# Arcade Screen Saver Framework

A very simple Python framework for making screen savers for Windows.  Uses the [Arcade](https://github.com/pythonarcade/arcade) library.


# Install and manually run screen saver example

    # From root of repo checkout...
    py -3 -m venv venv
    venv\Scripts\activate
    pip install -e .
    python -m arcade_screensaver_framework.examples.minimal_saver
    python -m arcade_screensaver_framework.examples.flying_lines
    python -m arcade_screensaver_framework.examples.oval_screensaver
    python -m arcade_screensaver_framework.examples.raindrops
    
    # add "/s" to any screen saver to launch it in fullscreen mode
    python -m arcade_screensaver_framework.examples.flying_lines /s


# How to install your screen saver to Windows 

    # cd into repo's top directory (not src\!)
    cd <MY_REPO>
    
    # Open a Windows Command Prompt with "Run as administrator" and 
    # run this command...
    install_screensaver src\arcade_screensaver_framework\examples\minimal_saver.py
    
    # Once complete, open up the "Screen Saver Settings" Windows dialog and
    # choose your screensaver from the dropdown list.
    
    # Note: The "Screen Saver Settings" dialog will feel very sluggish when your custom
    # screen saver is selected. This is because Windows is running the screen saver application
    # in the background as you click through the options in the dialog. Each run of the
    # application takes a couple seconds to complete.

![Hits](http://cc.amazingcounters.com/counter.php?i=3245831&c=9737806)
