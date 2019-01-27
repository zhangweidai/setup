echo "$Profile"
"$Profile"
function back {set-location ..}
New-Alias b back
New-Alias hi history


function echopath_impl {$env:path.split(";")}
New-Alias echopath echopath_impl

function gosetup {set-location $env:UserProfile\Documents\setup}
New-Alias cds gosetup

Set-PSReadlineOption -BellStyle None
New-Alias which get-command

function editrc {gvim "$Profile"}
New-Alias vcs editrc

function editrc {python $env:UserProfile\Documents\setup\python\tf_check.py}
New-Alias welltf editrc

# Set-PSReadLineKeyHandler -Chord Ctrl+Shift+B -ScriptBlock {
#     [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
#     [Microsoft.PowerShell.PSConsoleReadLine]::Insert('build')
#     [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
# }
Set-PSReadLineKeyHandler -Chord Ctrl+U -ScriptBlock {
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
}

Set-PSReadLineKeyHandler -Chord Ctrl+Shift+T -ScriptBlock {
    start-process powershell.exe
}
