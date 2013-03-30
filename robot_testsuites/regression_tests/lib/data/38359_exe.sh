#!/bin/sh

MAX=$1

i=0
while [ $i -lt $MAX ]; do
    echo -n "1" >> out1
		echo -n "2" >> out2
		echo -n "3" >> out3
		echo -n "4" >> out4
    i=$[$i + 1]
done


i=200
while [ $i -lt 100 ]; do
    echo -n "1" >> out1
    echo -n "2" >> out2
    echo -n "3" >> out3
    echo -n "4" >> out4
    i=$[$i + 1]
done
