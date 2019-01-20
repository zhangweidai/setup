#SingleInstance force

GroupAdd, AdobeMMButton, ahk_exe Photoshop.exe
GroupAdd, AdobeMMButton, ahk_exe Illustrator.exe
GroupAdd, AdobeMMButton, ahk_exe AcroRD32.exe
GroupAdd, AdobeMMButton, ahk_exe Acrobat.exe


; ^control +shift !alt

!^+l::
MsgBox, "Reloading Illustrator"
Reload 
Return


IsSuspended := False
+Esc:: 
Suspend, Toggle 
Suspend, Permit ;  very first line
MouseGetPos, xpos, ypos 
IsSuspended := !IsSuspended
TipText := IsSuspended ? "Script Suspended" : "Script Enabled"
ToolTip %TipText%, xpos, ypos
SetTimer, RemoveToolTip, -500
Return

#IfWinActive ahk_exe illustrator.exe
{
c::
Send, {Shift Down}
Send, n
Send, {Shift Up}
Return

x::
Send, {Delete}
Return

a::
SendInput, ^+a
Return

g::
Send, m
Return

}

;for every Adobe app where you want to use this trick


; If window is Adobe, Use middle button as an equivalent of hand tool
#IfWinActive ahk_group AdobeMMButton
{
WheelUp::
SendInput, {LAlt Down}{WheelUp 1}{LAlt Up}
Return
WheelDown::
SendInput, {LAlt Down}{WheelDown 1}{LAlt Up}
Return

+MButton::
MButton::
    Send {Space Down}{LButton Down}
    Keywait, MButton
    Send {LButton Up}{Space Up}
    Return
}

RemoveToolTip:
ToolTip
return
