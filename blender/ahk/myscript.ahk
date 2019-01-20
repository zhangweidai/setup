#SingleInstance force
; SendMode Input

; ^control +shift !alt #win 
; & 	An ampersand may be used between any two keys or mouse buttons to combine them into a custom hotkey. See below for details.
; * Wildcard: Fire the hotkey even if extra modifiers are being held down. This is often used in conjunction with remapping keys or buttons. For example: *#c:: ; Win+C, Shift+Win+C, Ctrl+Win+C, etc. will all trigger this hotkey.
; ~When the hotkey fires, its key's native function will not be blocked (hidden from the system). In both of the below examples, the user's click of the mouse button will be sent to the active window:
; $ This is usually only necessary if the script uses the Send command to send the keys that comprise the hotkey itself, which might otherwise cause it to trigger itself. The $ prefix forces the keyboard hook to be used to implement this hotkey, which as a side-effect prevents the Send command from triggering it. The $ prefix is equivalent to having specified #UseHook somewhere above the definition of this hotkey.


global lastop, sca_x, sca_y
sca_x := 3454
sca_y := 1064

; if ErrorLevel
;     ExitApp
; Editor := "C:\Program Files (x86)\Vim\vim81\gvim.exe"
; RegWrite REG_SZ, HKCR, AutoHotkeyScript\Shell\Edit\Command,, "%Editor%" "`%1"

GroupAdd, REMOTE_DESKTOPS, ahk_class Photoshop
GroupAdd, REMOTE_DESKTOPS, ahk_class illustrator
GroupAdd, REMOTE_DESKTOPS, ahk_exe blender.exe

GroupAdd, WINSHELLS, ahk_exe cmd.exe
GroupAdd, WINSHELLS, ahk_exe powershell.exe
GroupAdd, WINSHELLS, ahk_exe gvim.exe
; GroupAdd, WINSHELLS, ahk_exe bash.exe
GroupAdd, WINSHELLS, ahk_exe Explorer.exe
GroupAdd, WINSHELLS, ahk_exe chrome.exe
GroupAdd, WINSHELLS, ahk_exe firefox.exe

SetWinDelay,2
CoordMode,Mouse

Capslock::Ctrl	

#1::
WinActivate, ahk_exe blender.exe
MouseMove, %sca_x%, %sca_y%
MouseClick 
SendInput, {Shift Down}{Enter}{Shift Up}
SendRaw, import importlib
SendInput, {enter}
SendRaw, import utils
SendInput, {enter}
SendRaw, importlib.reload(utils)
SendInput, {enter}
SendRaw, from utils import *
SendInput, {enter}
SendRaw, well()
SendInput, {enter}
Return


#2::
MsgBox, %sca_x%, %sca_y%
Return

F7::
Run, C:\Program Files (x86)\Vim\vim81\gvim.exe %A_ScriptName%
Return

!^+l::
MsgBox, "Reloaded"
Reload 
return

^+l::
Reload 
return

#g::
SendInput, {RWin Down}
SendInput, {RWin Up}
Send, gvim
SendInput, {enter}
return

#n::
MouseMove, %sca_x%, %sca_y%
MouseClick 
return

#b::
Run, C:\Windows\System32\bash.exe ~
return

#h::
Run, chrome
return


; #If (toggle_state)
; {
#NumpadUp::MouseMove, 0, -75, 0, R  ; Win+UpArrow hotkey => Move cursor upward
+#NumpadUp::MouseMove, 0, -25, 0, R  ; Win+UpArrow hotkey => Move cursor upward
#NumpadDown::MouseMove, 0, 75, 0, R  ; Win+DownArrow => Move cursor downward
+#NumpadDown::MouseMove, 0, 25, 0, R  ; Win+DownArrow => Move cursor downward
#NumpadClear::MouseMove, 0, 75, 0, R  ; Win+DownArrow => Move cursor downward
+#NumpadClear::MouseMove, 0, 25, 0, R  ; Win+DownArrow => Move cursor downward
#NumpadLeft::MouseMove, -75, 0, 0, R  ; Win+LeftArrow => Move cursor to the left
#NumpadRight::MouseMove, 75, 0, 0, R  ; Win+RightArrow => Move cursor to the right
+#NumpadLeft::MouseMove, -25, 0, 0, R  ; Win+LeftArrow => Move cursor to the left
+#NumpadRight::MouseMove, 25, 0, 0, R  ; Win+RightArrow => Move cursor to the right

#NumpadHome::  ; LeftWin + RightControl => Left-click (hold down Control/Shift to Control-Click or Shift-Click).
*<#RCtrl::  ; LeftWin + RightControl => Left-click (hold down Control/Shift to Control-Click or Shift-Click).
SendEvent {Blind}{LButton down}
KeyWait RCtrl  ; Prevents keyboard auto-repeat from repeating the mouse click.
SendEvent {Blind}{LButton up}
return
; *<#AppsKey::  ; LeftWin + AppsKey => Right-click
#NumpadPgUp::  ; LeftWin + RightControl => Left-click (hold down Control/Shift to Control-Click or Shift-Click).
SendEvent {Blind}{RButton down}
KeyWait AppsKey  ; Prevents keyboard auto-repeat from repeating the mouse click.
SendEvent {Blind}{RButton up}
return
; }


^+!e::
Run explorer.exe
Return

^+!j::
InputBox, Operation, ,"setclickarea (sca)?" ,,,,,,,, %lastop%
lastop=%Operation%

if ErrorLevel
    return

if (Operation == "c")
{
    MouseClick 
}
else if (Operation == "ca")
{
    MouseMove, %sca_x%, %sca_y%
    MouseClick 
}

else if (Operation == "sca")
{
  MouseGetPos, sca_x, sca_y
}
return


; WHAT : edit clipboard path
^+v::
Run, gvim.exe %ClipBoard% ; Convert to plain text
return


; WHAT : reload blender load script
^l::
SetTitleMatchMode 3
WinActivate, Blender
SetControlDelay 2
;MouseMove, XXX2, YYY2
MouseMove, 1560, 1421
SetControlDelay 1
ControlClick 
SetControlDelay 1

;MouseMove, XXX, YYY
MouseMove, 1460, 1471
MouseClick 
SetControlDelay 2
MouseClick 
SetControlDelay 1

;MouseMove, XXX2, YYY2
MouseMove, 1560, 1421
SendInput, !p
Return

; F1::
; MsgBox, "Ok"
; Return

F13::
clipsaved:= Clipboard
IfInString, clipsaved, .bat
{
    Run, %clipsaved%
}
return

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

^+w::
WinClose
return
}

#IfWinActive ahk_exe bash.exe
{
^u::
SendInput, ^+u
return

^+w::
WinClose
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

; WHAT : regen blender load script
#IfWinActive ahk_exe blender.exe
{

f6::
SendInput, ^!u
Return

^+a::
MouseGetPos, xpos, ypos 
MsgBox, The cursor is at X%xpos% Y%ypos%.
Run, python.exe "C:\Users\Peter\Documents\GitHub\setup\blender\scripts\regen_blender_script.py" %xpos% %ypos%
Reload 
return

^u::
SendInput, {Shift Down}{Enter}{Shift Up}
return
}

