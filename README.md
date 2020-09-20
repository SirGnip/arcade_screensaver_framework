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
    cd ...
       
    # Run this from a Windows Command Prompt opened as administrator
    # First argument: path to screen saver script
    # Second arg: name of screen saver script with NO .py extension
    install_screensaver.bat src\arcade\screensaver_framework minimal_saver
    
    # Once complete, open up the ""Screen Saver Settings" Windows dialog and
    # choose your screensaver from the dropdown list.  
