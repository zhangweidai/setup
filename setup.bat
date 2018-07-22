if exist %~dp0.vimrc (
    copy %~dp0\.vimrc %HOMEPATH%\_vimrc
    copy %~dp0\_gvimrc %HOMEPATH%\_gvimrc
    xcopy %~dp0\.vim %HOMEPATH%\vimfiles /O /X /E /H /K
    mkdir %HOMEPATH%\GitHub
    mklink /D /J "%USERPROFILE%\Documents\GitHub\setup" "%USERPROFILE%\AppData\Local\lxss\root\setup"
)
