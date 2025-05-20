@echo off
echo Backing up Desktop...
xcopy "%USERPROFILE%\Desktop" "%USERPROFILE%\Desktop_Backup" /s /i /y
echo Done!
pause
