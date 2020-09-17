# Arcade Screen Saver Framework

A very simple Python framework for making screen savers for Windows.  Uses the [Arcade](https://github.com/pythonarcade/arcade) library.


# Install and manually run screen saver example

    # From root of repo checkout...
    py -3 -m venv venv
    venv\Scripts\activate
    pip install -e .
    python -m arcade_screensaver_framework.minimal_saver


# How to install your screen saver to Windows 

    # cd into repo's top directory (not src!)
    # venv must be active
    pip install pyinstaller
    
    # run from a Windows Command prompt
    make_screensaver.bat
    
    # Run from a Windows Command Prompt opened as administrator
    move_screensaver_as_admin.bat
    
    # Choose your screensaver from "Screen Saver Settings" Windows dialog 


# How to make your own screen saver...
