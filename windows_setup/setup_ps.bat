@echo off
REM if exist %HOMEPATH%\_vimrc (
REM     del %HOMEPATH%\_vimrc
REM )
REM mklink "%HOMEPATH%\_vimrc" "%~dp0\.vimrc" 
REM 
REM if exist %HOMEPATH%\_gvimrc (
REM     del %HOMEPATH%\_gvimrc
REM )
REM mklink "%HOMEPATH%\_gvimrc" "%~dp0\_gvimrc" 
REM 
REM if not exist %HOMEPATH%\vimfiles (
REM     mklink /D /J "%HOMEPATH%\vimfiles" "%~dp0\.vim" 
REM )
REM xcopy /s %~dp0\windows_setup\Microsoft.PowerShell_profile.ps1 %USERPROFILE%\Documents\WindowsPowerShell\
set dest= "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" 
set src="%~dp0\Microsoft.PowerShell_profile.ps1"

REM echo %dest%
REM if exist %dest% (
REM      ren %dest% newname
REM )

if not exist %src% (
   echo "source does not exist
   echo %src%
   exit
)

if not exist %dest% (
    mklink %dest% %src%
)

pause
REM if exist %~dp0.vimrc (
REM     echo "starting"
REM     mklink "%HOMEPATH%\_gvimrc" "%~dp0\_gvimrc" 
REM     mklink /D /J "%HOMEPATH%\vimfiles" "%~dp0\.vim" 
REM    mklink "C:\Users\Peter\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\myscript.ahk" "%~dp0\blender\ahk\myscript.ahk" 
REM )
