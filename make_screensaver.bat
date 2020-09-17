call venv\Scripts\activate
del /S /Q build dist
pyinstaller src\arcade_screensaver_framework\minimal_saver.py --add-binary "venv\Lib\site-packages\pymunk\chipmunk.dll;." --add-binary "venv\Lib\site-packages\arcade\soloud\soloud*.dll;.\arcade\soloud" --add-data "venv\Lib\site-packages\arcade\resources;.\arcade\resources" --windowed --onefile
copy dist\minimal_saver.exe dist\minimal_saver.scr
