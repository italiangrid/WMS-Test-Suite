#!/bin/sh

MAX=$1

i=0
while [ $i -lt $MAX ]; do
		echo -n "1" >> out1
		echo -n "2" >> out2
    i=$[$i + 1]
done