@REM This script must be executed from a command prompt run "as administrator".
@REM Change current working directory to the root of this repo before running this script.
@REM First command line argument is the path to your screen saver entry point
@REM Second command line argument is the base name of your screen saver script (NO .py extension)
@REM
@REM   Example: install_screensaver.bat src\arcade_screensaver_framework minimal_saver
@echo on

@echo ===== Input =====
@echo Path: %1
@echo Base filename: %2
@echo Using %1\%2.py to generate and install a screen saver

@echo.
@echo.
@echo ===== Activate virtual environment =====
call venv\Scripts\activate
@echo on
where python

@echo.
@echo.
@echo ===== Remove any existing pyinstaller build or dist directories =====
rmdir /S /Q build dist

@echo.
@echo.
@echo ===== Run pyinstaller to make .exe =====
pyinstaller %1\%2.py --windowed --onefile
echo.
dir dist\

@echo.
@echo.
@echo ===== Copy %2.exe to Windows\System32 as a .scr file =====
copy dist\%2.exe dist\%2.scr
move dist\%2.scr c:\Windows\System32\
@echo.
dir c:\Windows\System32\*.scr