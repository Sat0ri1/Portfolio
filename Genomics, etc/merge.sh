#!/bin/bash
mkdir merged

for file in dane/*.txt
do 
	cat $file
	echo
done > sequences.txt
mv -f sequences.txt merged
