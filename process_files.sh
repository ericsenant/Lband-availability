#!/bin/bash
FILES="./list_files"

while IFS= read -r file
do
        [ -f "$file" ]
        echo "Processing $file file..."
        cat $file | sbp2json | jq -c "select(.msg_type==528 or .msg_type==30583 or .msg_type==522)" > $file.json
        python3 ~/Documents/Lband/LTE-LBand-complementarity.py $file.json
        open $file.json_1Hz.kml
done < "$FILES"
