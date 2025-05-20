@echo off
echo Searching for large files (>100MB)...
forfiles /p %USERPROFILE% /s /m *.* /c "cmd /c if @fsize GEQ 104857600 echo @path @fsize" > "%USERPROFILE%\large_files.txt"
notepad "%USERPROFILE%\large_files.txt"
