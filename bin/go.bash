#!/bin/bash
if [ $# == 1 ];
then
    bar=`python ~/setup/python/go.py $1`
    echo $bar
    cd "$bar"
else
    python ~/setup/python/go.py 
fi
