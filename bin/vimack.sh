#!/bin/sh

sed -i "1i$1" $TS/search_history.list
rg -i --hidden --follow --color always -C 1 "$1" --no-heading -n -g "!Makefile*" >& $TS/prevGrepResults
cat -n $TS/prevGrepResults
cat $TS/prevGrepResults | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" > $TS/prevGrepResults.noColor

