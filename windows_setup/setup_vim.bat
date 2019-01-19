@echo off
if exist %HOMEPATH%\_vimrc (
    del %HOMEPATH%\_vimrc
)
mklink "%HOMEPATH%\_vimrc" "%~dp0\.vimrc" 

if exist %HOMEPATH%\_gvimrc (
    del %HOMEPATH%\_gvimrc
)
mklink "%HOMEPATH%\_gvimrc" "%~dp0\_gvimrc" 

if not exist %HOMEPATH%\vimfiles (
    mklink /D /J "%HOMEPATH%\vimfiles" "%~dp0\.vim" 
)


REM if exist %~dp0.vimrc (
REM     echo "starting"
REM     mklink "%HOMEPATH%\_gvimrc" "%~dp0\_gvimrc" 
REM     mklink /D /J "%HOMEPATH%\vimfiles" "%~dp0\.vim" 
REM    mklink "C:\Users\Peter\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\myscript.ahk" "%~dp0\blender\ahk\myscript.ahk" 
REM )
