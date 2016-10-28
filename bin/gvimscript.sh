#!/bin/sh
echo $1
`echo $1 | awk -f $HOME/setup/bin/gvi_line`
