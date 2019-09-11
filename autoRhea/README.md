# Rhea, Rscript edition

Normalize
```
Rscript normalize.R   Raw_OtuTable  Output_dir
```


Alpha diversity
```
Rscript alpha.R  Normalized_OtuTable Output_dir
```

## USEARCH analysis


### tree
```
usearch -calc_distmx zotus.fa -tabbedout mx.txt -maxdist 0.2 -termdist 0.3
usearch -cluster_aggd mx.txt -treeout clusters.tree -clusterout clusters.txt  -id 0.80 -linkage min
```
