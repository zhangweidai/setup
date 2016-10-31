#!/bin/bash

#sed -i "1i$1" $TS/search_history.list
bar=`which rg`
if [ "$bar" == "" ];
then
   ag --hidden --follow -C 1 "$1" >& $TS/prevGrepResults
   else
   rg -i --hidden --follow --color always -C 1 "$1" --no-heading -n >& $TS/prevGrepResults
fi

cat -n $TS/prevGrepResults
cat $TS/prevGrepResults | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" > $TS/prevGrepResults.noColor

