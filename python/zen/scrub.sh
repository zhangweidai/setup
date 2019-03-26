#!/bin/bash
cd ../zen_dump/toscrub

if [ "$1" == "Derivatives" ];
then
    find . -type f | xargs sed -i /$1/d >& /dev/null
elif [ "$1" != "Ticker" ];
then
# find . -type f | xargs sed -i '/"UBFUT"/d'
# find . -type f | xargs sed -i '/"FTI"/d'
# find . -type f | xargs sed -i '/"STX"/d'
# find . -type f | xargs sed -i '/"EVRG"/d'
    find . -type f | xargs sed -i /\"$1\"/d >& /dev/null
    find . -type f | xargs sed -i /^$1/d >& /dev/null
    rm ../historical/$1.csv >& /dev/null
fi
