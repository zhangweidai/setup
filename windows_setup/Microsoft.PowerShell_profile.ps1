echo "$Profile"
"$Profile"
function back {set-location ..}
New-Alias b back
New-Alias hi history

$env:SETUP = "C:\Users\Peter\Documents\setup"

function gosetup {set-location $env:SETUP}
New-Alias cds gosetup

Set-PSReadlineOption -BellStyle None
New-Alias which get-command

function editrc {gvim "$Profile"}
New-Alias vcs editrc

function editrc {python $env:SETUP\python\tf_check.py}
New-Alias welltf editrc

