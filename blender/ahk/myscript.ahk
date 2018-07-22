#SingleInstance force

; ^control +shift !alt

GroupAdd, REMOTE_DESKTOPS, ahk_class Photoshop
GroupAdd, REMOTE_DESKTOPS, ahk_class illustrator
GroupAdd, REMOTE_DESKTOPS, ahk_exe blender.exe
GroupAdd, WINSHELLS, ahk_exe cmd.exe
GroupAdd, WINSHELLS, ahk_exe powershell.exe
return

SetWinDelay,2
CoordMode,Mouse
return

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
WinGetActiveTitle, title
WinGet, maximized, MinMax, %title%
if (maximized)
   WinRestore, %title%
else
   WinMaximize, %title%
return


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
!LButton::

CoordMode, Mouse, Relative
MouseGetPos, cur_win_x, cur_win_y, window_id
WinGet, window_minmax, MinMax, ahk_id %window_id%

; Return if the window is maximized or minimized
if window_minmax <> 0
{
  return
}

CoordMode, Mouse, Screen
SetWinDelay, 0

loop
{
  ; exit the loop if the left mouse button was released
  if !GetKeyState("LButton", "P")
  {
    break
  }

  ; move the window based on cursor position
  MouseGetPos, cur_x, cur_y
  WinMove, ahk_id %window_id%,, (cur_x - cur_win_x), (cur_y - cur_win_y)
}

return
}
#IfWinActive ahk_group WINSHELLS
{
^u::
SendInput, {Esc}
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

