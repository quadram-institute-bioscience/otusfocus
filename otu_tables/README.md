# OTU tables

This directory contains raw OTU tables (TSV)


## Detection of cross talk using USEARCH 
See [documentation](https://drive5.com/usearch/manual/cmd_otutab_xtalk.html).
```
# Make OTU table
usearch -otutab reads.fq -otus zotus.fa -otutabout otutab.tsv 

# Denoise OTU table
usearch -otutab_xtalk otutab.tsv -otutabout otutab_denoised.tsv  \
  -report xtalk_summary.txt -htmlout xtalk_view.html 
```

