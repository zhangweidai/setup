#!/bin/bash
cd ../zen_dump/holdings
if [ "$1" != "Ticker" ];
then
# find . -type f | xargs sed -i '/"UBFUT"/d'
# find . -type f | xargs sed -i '/"FTI"/d'
# find . -type f | xargs sed -i '/"STX"/d'
# find . -type f | xargs sed -i '/"EVRG"/d'
    find . -type f | xargs sed -i /\"$1\"/d
    find . -type f | xargs sed -i /^$1/d
    rm ../historical/$1.csv
fi
