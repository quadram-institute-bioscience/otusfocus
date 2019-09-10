#!/usr/bin/env Rscript
packages <-c("ade4","GUniFrac","phangorn","cluster","microbiome",
             "fpc","compare","plotrix","PerformanceAnalytics","reshape","ggplot2","gridExtra","grid","ggrepel",
             "gtable","Matrix","cowplot", "Hmisc","corrplot","muStat")

# Function to check whether the package is installed
InsPack <- function(pack)
{
  if ((pack %in% installed.packages()) == FALSE) {
     cat("ERROR: Missing package ", pack, "\n")
  } 
}



# Applying the installation on the list of packages
packs <- lapply(packages, InsPack)

