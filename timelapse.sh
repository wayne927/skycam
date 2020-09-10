#!/bin/bash

file=static/raspistill_out.txt
rm -f $file

for i in {1..20}
do
    echo $i >> $file
    sleep 1
done
