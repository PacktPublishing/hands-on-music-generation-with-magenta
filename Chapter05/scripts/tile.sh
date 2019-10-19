#!/usr/bin/env bash

for filename in $( ls *.png )
do
    echo "Processing file $filename"

    # Trims the white space around the plot
    filename_trim="${filename%.*}_trim.png"
    convert -trim "${filename}" "${filename_trim}"

    # Adds border for a white padding
    filename_border="${filename_trim%.*}_border.png"
    convert -border 5x5 "${filename_trim}" "${filename_border}"
done

filenames=$( ls *_border.png )
filename_tile=tile.png
echo "Tiling in ${filename_tile} files:"
echo "${filenames}"
convert ${filenames} +append ${filename_tile}

