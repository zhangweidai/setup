#NoEnv 
#SingleInstance force
SetWorkingDir, %A_ScriptDir% 
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetDefaultMouseSpeed, 25
SetMouseDelay, 20

InputBox, UserInput, pass, pass
if ErrorLevel
{
    MsgBox, CANCEL was pressed.
    exit
}

startfidelity("torytat", UserInput)
save_port("tory_ports.csv")
save_order("tory_order.csv")
exitfidelity()

startfidelity("zhangweidai", UserInput)
save_port("peter_ports.csv")
save_order("peter_order.csv")
exitfidelity()

return

startfidelity(username, password)
{
    sleep,100
    WinActivate, ahk_exe ActiveTraderPro.exe
    sleep,100
    IfWinNotActive, ahk_exe ActiveTraderPro.exe
    {
        sleep,100
        Run, C:\Users\Zoe\Desktop\fidelity
        sleep,2000
        WinActivate, ahk_exe ActiveTraderPro.exe
        sleep,2000
    }
    IfWinNotActive, ahk_exe ActiveTraderPro.exe
    {
        MsgBox "Not active"
        exit
    }
    WinActivate, ahk_exe ActiveTraderPro.exe
    sleep,100
    WinMaximize, ahk_exe ActiveTraderPro.exe
    sleep,500
    Send, %username%
    sleep, 200
    Send, {tab}
    sleep, 200
    Send, %password%
    sleep, 200
    Send, {Enter}
    sleep, 8200
    
    WinActivate, ahk_exe ActiveTraderPro.exe
    sleep,1000
    WinMaximize, ahk_exe ActiveTraderPro.exe
    sleep,1000
    return
}

exitfidelity()
{
    sleep,2000
    Send !{f4}
    sleep,2000
    IfWinActive, ahk_exe ActiveTraderPro.exe
    {
        Send !{f4}
        sleep,1000
    }
    return
}

save_order(file)
{
    sleep,2000
    MouseClick,, 90, 70
    sleep,1500
    MouseClick, right, 900, 700
    Send, {Up}
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Right}
    sleep,200
    Send, {Enter}
    sleep,1200
    Send, %file%
    sleep,1200
    Send, {ENTER}
    sleep,1200
    Send, {ENTER}
    sleep,2000
    MouseClick,, 1833, 131
    sleep,1000
    return
}

save_port(file)
{
    sleep,500
    WinActivate, ahk_exe ActiveTraderPro.exe
    WinMaximize, ahk_exe ActiveTraderPro.exe
    DllCall("SetCursorPos", int, 0, int, 0)
    sleep,500
    DllCall("SetCursorPos", int, 250, int, 72)
    sleep,500
    DllCall("mouse_event", uint, 2, int, x, int, y, uint, 0, int, 0)
    MouseClick,, 250, 72
    sleep,500
    MouseClick,, 300, 125
    sleep,1500
    MouseClick,, 300, 125
    sleep,1500
    Send, {Down}
    sleep,500
    Send, {Right}
    sleep,500
    Send, {Enter}
    sleep,1500
    MouseClick, , 900, 700
    sleep,500
    MouseClick, right, 900, 700
    sleep,100
    DllCall("SetCursorPos", int, 250, int, 72)
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Up}
    sleep,200
    Send, {Right}
    sleep,200
    Send, {Enter}
    sleep,1200
    Send, %file%
    sleep,1200
    Send, {Enter}
    sleep,1200
    Send, {Enter}
    sleep,1200
    MouseClick,, 1676, 125
    sleep,200
    return
}

!Escape::
ExitApp
Return
