#!/bin/bash
cd holdings
# find . -type f | xargs sed -i '/"UBFUT"/d'
# find . -type f | xargs sed -i '/"FTI"/d'
# find . -type f | xargs sed -i '/"STX"/d'
# find . -type f | xargs sed -i '/"EVRG"/d'
find . -type f | xargs sed -i '/"Futures"/d'
