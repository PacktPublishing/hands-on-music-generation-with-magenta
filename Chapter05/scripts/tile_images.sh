#!/usr/bin/env bash

readonly PROGNAME=$(basename $0)

USAGE="\nUsage: ./${PROGNAME} sourceDirectory
\t
\tTiles the png files in the sourceDirectory by taking each
\timage, trimming the white space, adding a 5 pixel white border, and
\tappending them horizontally. The resulting images will be in the
\tsourceDirectory.
\t
\tRequires imagemagick (convert).
\t"
if [ $# -ne 1 ]; then
  echo -e "${USAGE}"
  exit 1
else
  SOURCE_DIRECTORY="$1"
fi

function tile_images() {
  for filename in *.png; do
    echo "Processing file $filename"

    # Trims the white space around the plot
    filename_trim="${filename%.*}_trim.png"
    convert -trim "${filename}" "${filename_trim}"

    # Adds border for a white padding
    filename_border="${filename_trim%.*}_border.png"
    convert -border 5x5 "${filename_trim}" "${filename_border}"
  done

  filenames=$(ls *_border.png)
  filename_tile="tile.png"
  echo "Tiling in ${filename_tile} files:"
  echo "${filenames}"
  convert ${filenames} +append ${filename_tile}
}

WORKING_DIRECTORY=$(pwd)
cd "${SOURCE_DIRECTORY}" || exit
tile_images
cd "${WORKING_DIRECTORY}" || exit
