#!/bin/bash
echo Ripping pictures...
for file in *.PIC
do
    echo Ripping $file...
    python3 dinoparkpic.py $file
done

echo Ripping palettes...
for file in *.PIC
do
    echo Ripping $file...
    python3 dinoparkpal.py $file
    python3 dinoparkpal.py OFFICE.PIC 10
done

echo Ripping sprites...
while read line
do
    actfile=$(echo $line | cut -d ' ' -f 1)
    palette=$(echo $line | cut -d ' ' -f 2)
    echo Ripping $actfile...
    python dinoparkact.py $actfile $palette
done < files
