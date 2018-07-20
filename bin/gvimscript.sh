#!/bin/bash
echo $1
export myvim='vim'
if [ "${MGC_DEBUG_FLAGS}" == "1" ]; then
    export myvim='gvim'
fi
export cmd=`echo $1 | awk -f $HOME/setup/bin/gvi_line`
export cmd="$myvim $cmd"
`echo $cmd`
# 
# `gvim echo $1 | awk -f $HOME/setup/bin/gvi_line`
# else
# `vim echo $1 | awk -f $HOME/setup/bin/gvi_line`
# fi
