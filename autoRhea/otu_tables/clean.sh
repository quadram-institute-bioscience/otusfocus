#!/bin/bash
if [ "NO$1" == "NO" ];
then
	INPUT=otutab.tsv
else
	INPUT=$1
fi

DIR=$(dirname $INPUT)
usearch -otutab_xtalk "$INPUT" -otutabout $DIR/otutab_denoised.tsv  \
  -report $DIR/xtalk_summary.txt -htmlout $DIR/xtalk_view.html

usearch -otutab_stats "$INPUT" -output $DIR/otutab.stats.txt
