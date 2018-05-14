if exist %~dp0.vimrc (
     mklink "%HOMEPATH%\_vimrc" "%~dp0\.vimrc" 
     mklink "%HOMEPATH%\_gvimrc" "%~dp0\_gvimrc" 
REM     mklink /D /J "%HOMEPATH%\vimfiles" "%~dp0\.vim" 
REM    mklink "C:\Users\Peter\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\myscript.ahk" "%~dp0\blender\ahk\myscript.ahk" 
)
