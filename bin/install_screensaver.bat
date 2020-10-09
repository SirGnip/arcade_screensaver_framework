@echo off
echo A few things to check before allowing this script to continue:
echo.
echo 1) This script *must* be executed from a Command Prompt window that was
echo    started with "Run as administrator". Otherwise, this script will not
echo    have the necessary permissions to copy your screen saver to the
echo    \Windows\System32 system directory.
echo.
echo 2) If your screen saver is running from a virtual environment, that
echo    environment must be active before running this script.
echo.
echo 3) Ensure the .py file containing your screen saver is passed as an
echo    argument to this script:
echo.
echo       Example: install_screensaver src\arcade_screensaver_framework\examples\minimal_saver.py
echo.
pause

echo.
echo Bundling and installing screen saver: %1
for /F %%i in ("%1") do set BASE_FILENAME=%%~ni

@echo on
@echo.
@echo.
@echo ===== Running pyinstaller to make bundled .exe =====
pyinstaller %1 --windowed --onefile
@if %errorlevel% neq 0 (
    @echo ERROR encountered. Details above...
    exit /b %errorlevel%
)

@echo.
@echo.
@set TARG_DIR=%SystemRoot%\System32
@echo ===== Copying dist\%BASE_FILENAME%.exe to %TARG_DIR% as a .scr file =====
copy dist\%BASE_FILENAME%.exe dist\%BASE_FILENAME%.scr
@if %errorlevel% neq 0 (
    @echo ERROR encountered. Details above...
    exit /b %errorlevel%
)
move dist\%BASE_FILENAME%.scr %TARG_DIR%
@if %errorlevel% neq 0 (
    @echo ERROR encountered. Details above...
    exit /b %errorlevel%
)

@echo.
@echo.
@echo ===== Screen savers currently in %TARG_DIR%:
@dir %TARG_DIR%\*.scr
@echo.
@echo.
@echo COMPLETE! The new screen saver should now be available in Window's Screen
@echo Saver Settings dialog.
