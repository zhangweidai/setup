#!/bin/bash
export location=`pwd`/setup_ps.bat
export location=`wslpath -w $location`
powershell.exe -Command $location
