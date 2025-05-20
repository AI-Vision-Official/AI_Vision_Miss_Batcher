@echo off
set DOWNLOADS=%USERPROFILE%\Downloads
md "%DOWNLOADS%\Images"
md "%DOWNLOADS%\Documents"
md "%DOWNLOADS%\Other"
move "%DOWNLOADS%\*.jpg" "%DOWNLOADS%\Images"
move "%DOWNLOADS%\*.pdf" "%DOWNLOADS%\Documents"
move "%DOWNLOADS%\*.doc*" "%DOWNLOADS%\Documents"
echo Sorting complete!
pause
