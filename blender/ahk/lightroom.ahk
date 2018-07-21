#SingleInstance force

^+l::
Reload 

#IfWinActive ahk_exe lightroom.exe
x::
Send, {Delete}
SetControlDelay 1
SendRaw, d
SendRaw, d
WinActivate, ake_exe lightroom.exe
Return

a::
Send, {Right}
Return


l::
Send, {Right}
Return

e::
SendInput, !^2
Return


h::
Send, {Left}
Return

s::
SendInput, +^s
Return

j::
Send, {Down}
Return

k::
Send, {Up}
Return




^+Up::
MsgBox Up

