# OTU tables

This directory contains raw OTU tables (TSV)


## Detection of cross talk using USEARCH
```
usearch -otutab_xtalk otutab.tsv -report xtalk_summary.txt -htmlout xtalk_view.html -otutabout otutab_denoised.tsv
```

