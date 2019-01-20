@echo off
set dest= "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" 
set src="%~dp0\Microsoft.PowerShell_profile.ps1"

if not exist %src% (
   echo "source does not exist
   echo %src%
   exit
)

if not exist %dest% (
    mklink %dest% %src%
)

pause
