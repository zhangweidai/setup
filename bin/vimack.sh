#!/bin/bash

pysearch=""
csearch=0
filesonly=""
searchstr="$1"

while test $# -gt 0
do
    case "$1" in
        --py) pysearch="--py"
            ;;
        --files) 
        filesonly="--files"
        searchstr=""
            ;;
    esac
    shift
done

#sed -i "1i$1" $TS/search_history.list
wd=`pwd`
skipD=""

if [ -d ./all ]; then
    pysearch="--py"
elif [ -d ./zen ]; then
    pysearch="--py"
fi

#sed -i "1i$1" $TS/search_history.list
ag --hidden --follow -C 1 --color "${searchstr}" ${pysearch} >& $TS/prevGrepResults

cat -n $TS/prevGrepResults
cat $TS/prevGrepResults | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" > $TS/prevGrepResults.noColor

