#!/bin/sh
export MY_IWA
export MYVIM
echo $1
`echo $1 | awk -f $HOME/setup/bin/gvi_line`
