---
title: 'otusfocus: reduce the cross-talk noise in metabarcoding experiments'
tags:
  - genomics
  - bioinformatics
  - metabarcoding
  - cross-talk
  - illumina
  - sequencing
authors:
  - name: Andrea Telatin
    affiliation: 1
    orcid: 0000-0001-7619-281X
  - name: Giovanni Birolo
    affiliation: 2

affiliations:
  - name: Gut Microbes and Health Programme, Quadram Institute Bioscience, Norwich, UK
    index: 1
  - name: Dept. Medical Sciences, University of Turin, ITALY
    index: 2

date: "15 December 2019"
bibliography: paper.bib

---


# Summary

Illumina sequencing is the most widely adopted technology to perform metabarcoding experiments (_e.g._, @protocol). 
In a typical metabarcoding experiment, more than one hundred samples are multiplexed and run in the same sequencing run,
and due to the nature of the experiment it is expected to find the same sequence in multiple samples. 

Illumina sequencing, however, displays a technical bias resulting in a small fraction of sequences belonging 
to one sample being assigned to a different sample. 
This phenomenon, called *cross-talk* or *index hopping* [@illumina], can create a background noise in the
numerical output of the metabarcoding experiment (called *feature table*, or *OTU table*). 
A proposed method [@crosstalk] to reduce this problem is a stingent quality filtering on the barcode sequence 
(the fraction of the sequence used to identify the sample), 
but this doesn't take into account the cross-talk due to errors due to the 
imaging of very close sequencing clusters [@illuminawikipedia].

Robert Edgar, the author of the well-known USEARCH package for metabarcoding data analysis [@usearch], 
described a heuristic method for reduction of cross-talk directly from the feature table [@Edgar2018], 
under the assumption that the cross-talk observed is mainly due to leak of sequences
from a *reference sequence* (or feature) that is very abundant in one sample to other samples of the same sequencing run.

`otusfocus` is the Python implementation of the cross-talk reduction approach described by Rober Edgar in [@Edgar2018], and a set of corollary scripts to manage feature tables. 
Following the author's description of the *de novo* approach 
(*i. e.* not assuming that reference mock communities have been sequenced),
we implemented the two-step heuristic algorithm using Pandas [@pandas]: 
first a cross talk index is calculated using a set of candidate features and 
then the feature table is cleaned setting to zero the counts that are most likely to be due to cross-talk.

## Bibliography





