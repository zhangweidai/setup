@echo off 
setx userpath "C:\Users\Peter" /m
setx gits "%userpath%\Documents\GitHub" /m
setx myblender "%gits%\setup\blender" /m
setx bats "%myblender%\bats" /m
pause
