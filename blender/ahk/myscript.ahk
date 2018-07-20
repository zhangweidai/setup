#SingleInstance force


GroupAdd, REMOTE_DESKTOPS, ahk_class Photoshop
GroupAdd, REMOTE_DESKTOPS, ahk_class illustrator
GroupAdd, REMOTE_DESKTOPS, ahk_exe blender.exe
return

; ^control +shift !alt

^+l::
Reload 
return

!^+l::
Reload 
return




; WHAT : edit clipboard path
^+v::
Run, gvim.exe %ClipBoard% ; Convert to plain text
return

; WHAT : regen blender load script
^+a::
MouseGetPos, xpos, ypos 
MsgBox, The cursor is at X%xpos% Y%ypos%.
Run, python.exe "C:\Users\Peter\Documents\GitHub\setup\blender\scripts\regen_blender_script.py" %xpos% %ypos%
Reload 
return

; WHAT : reload blender load script
^l::
SetTitleMatchMode 3
WinActivate, Blender
SetControlDelay 2
;MouseMove, XXX2, YYY2
MouseMove, 950, 670
SetControlDelay 1
ControlClick 
SetControlDelay 1

;MouseMove, XXX, YYY
MouseMove, 850, 720
MouseClick 
SetControlDelay 2
MouseClick 
SetControlDelay 1

;MouseMove, XXX2, YYY2
MouseMove, 950, 670
SendInput, !p
Return

F1::
MsgBox, "Ok"
Return

F13::
;clipsaved:= Clipboard
;IfInString, clipsaved, .ahk
;{
;   MsgBox, %clipsaved%
;}
;return

SetTitleMatchMode 3
WinActivate, ahk_exe illustrator.exe
sleep 100
Send, !f
Send, r
Send, {up}
Send, {enter}
SendInput, ^v
Send, {enter}
Return

!^+m::
Send, {LWin down}
Send, {up}
Send, {LWin up}
Return

!^+o::
Run, "C:\Users\Peter\AppData\Local\Programs\Python\Python35\python.exe" "C:\Users\Peter\Documents\GitHub\setup\blender\py\opener.py" 
Return

^+w::
WinActivate, Blender
Return

; WHAT : copy to vim
^+q::
SetTitleMatchMode 3
WinActivate, Blender
SendInput, ^c
SendInput, ^c
SendInput, ^c
SetTitleMatchMode 2
WinActivate, GVIM
SendInput, ^+p
Return

#IfWinActive ahk_exe lightroom.exe
{
^+e::
SendRaw, from utils import copyToClipBoard
Send, {Enter}
SendRaw, copyToClipBoard()
Send, {Enter}
SetTitleMatchMode 2
WinActivate, GVIM
SendInput, ^+p
Reload 
Return
}

onecanon()
{
SendRaw, bc
MouseClick 
MouseMove, 10 , 210, , R
SetControlDelay 1
}

onepylon()
{
SendRaw, be
MouseClick 
MouseMove, 10 , 210, , R
SetControlDelay 1
}


#IfWinNotActive, ahk_group REMOTE_DESKTOPS
{
LWin & LButton::
CoordMode, Mouse  ; Switch to screen/absolute coordinates.
MouseGetPos, EWD_MouseStartX, EWD_MouseStartY, EWD_MouseWin
WinGetPos, EWD_OriginalPosX, EWD_OriginalPosY,,, ahk_id %EWD_MouseWin%
WinGet, EWD_WinState, MinMax, ahk_id %EWD_MouseWin% 
if EWD_WinState = 0  ; Only if the window isn't maximized 
    SetTimer, EWD_WatchMouse, 10 ; Track the mouse as the user drags it.
return

EWD_WatchMouse:
GetKeyState, EWD_LButtonState, LButton, P
if EWD_LButtonState = U  ; Button has been released, so drag is complete.
{
    SetTimer, EWD_WatchMouse, off
    return
}
GetKeyState, EWD_EscapeState, Escape, P
if EWD_EscapeState = D  ; Escape has been pressed, so drag is cancelled.
{
    SetTimer, EWD_WatchMouse, off
    WinMove, ahk_id %EWD_MouseWin%,, %EWD_OriginalPosX%, %EWD_OriginalPosY%
    return
}
; Otherwise, reposition the window to match the change in mouse coordinates
; caused by the user having dragged the mouse:
CoordMode, Mouse
MouseGetPos, EWD_MouseX, EWD_MouseY
WinGetPos, EWD_WinX, EWD_WinY,,, ahk_id %EWD_MouseWin%
SetWinDelay, -1   ; Makes the below move faster/smoother.
WinMove, ahk_id %EWD_MouseWin%,, EWD_WinX + EWD_MouseX - EWD_MouseStartX, EWD_WinY + EWD_MouseY - EWD_MouseStartY
EWD_MouseStartX := EWD_MouseX  ; Update for the next timer-call to this subroutine.
EWD_MouseStartY := EWD_MouseY
return
}

#IfWinActive ahk_exe Foxit Reader.exe
{
k::
SendInput, {up}
return

^k::
SendInput, {up}{up}{up}
return

j::
SendInput, {down}
return

^j::
SendInput, {down}{down}{down}
return
}

