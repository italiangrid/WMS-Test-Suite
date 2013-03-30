#!/bin/bash

echo "Hi all, this is a perusal test program..."

for (( i=0 ; $i < 50 ; i = $(($i + 1)) )); do

	echo "Step number $i"
	date
	sleep 30

done

echo ""
echo "Bye"


