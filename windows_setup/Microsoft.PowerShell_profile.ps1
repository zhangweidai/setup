function Do-ActualThing {
    code $profile
}

function Do-ActualThing2 {
    cd \\wsl$\Ubuntu-20.04\home\peter\setup
}
function profilesetup {
    . $profile
}

function back {
    cd ..
}

If (-Not (Test-Path Variable:PSise)) {  # Only run this in the console and not in the ISE
    Import-Module Get-ChildItemColor
    
    Set-Alias l Get-ChildItem -option AllScope
    Set-Alias ls Get-ChildItemColorFormatWide -option AllScope
    Set-Alias vcs Do-ActualThing
    Set-Alias cds Do-ActualThing2
    Set-Alias pro profilesetup
    Set-Alias b back
}

Set-PSReadLineKeyHandler -Chord Ctrl+u -ScriptBlock {
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
#    [Microsoft.PowerShell.PSConsoleReadLine]::Insert('build')
#    [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
}
Set-PSReadLineOption -EditMode Emacs

