#!/bin/bash
if [ "NO$1" == "NO" ];
then
	INPUT=otutab.tsv
else
	INPUT=$1
fi
usearch -otutab_xtalk $INPUT -otutabout otutab_denoised.tsv  \
  -report xtalk_summary.txt -htmlout xtalk_view.html
