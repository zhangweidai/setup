@echo off
if exist %USERPROFILE%\_vimrc (
    del %USERPROFILE%\_vimrc
)
mklink "%USERPROFILE%\_vimrc" "%~dp0\.vimrc" 

if exist %USERPROFILE%\_gvimrc (
    del %USERPROFILE%\_gvimrc
)
mklink "%USERPROFILE%\_gvimrc" "%~dp0\_gvimrc" 

if not exist %USERPROFILE%\vimfiles (
    mklink /D /J "%USERPROFILE%\vimfiles" "%~dp0\.vim" 
)


REM if exist %~dp0.vimrc (
REM     echo "starting"
REM     mklink "%USERPROFILE%\_gvimrc" "%~dp0\_gvimrc" 
REM     mklink /D /J "%USERPROFILE%\vimfiles" "%~dp0\.vim" 
REM    mklink "C:\Users\Peter\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\myscript.ahk" "%~dp0\blender\ahk\myscript.ahk" 
REM )
