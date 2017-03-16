---
title: 'SaffronTree: Fast, reference-free pseudo-phylogenomic trees from reads or contigs.'
tags:
  - bioinformatics
  - phylogenetics
  - bacteria
authors:
 - name: Andrew J. Page
   orcid: 0000-0001-6919-6062
   affiliation: Pathogen Informatics, Wellcome Trust Sanger Institute
 - name: Martin G. Hunt
   orcid: 0000-0002-8060-4335
   affiliation: Pathogen Informatics, Wellcome Trust Sanger Institute
 - name: Torsten Seemann
   orcid: 0000-0001-6046-610X
   affiliation: University of Melbourne
 - name: Jacqueline A. Keane
   orcid: 0000-0002-2021-1863
   affiliation: Pathogen Informatics, Wellcome Trust Sanger Institute
  
date: 9 Mar 2017
bibliography: paper.bib
---

# Summary
When defining bacterial populations through whole genome sequencing (WGS) the samples often have unknown evolutionary histories.  With the increased use of next generation WGS in routine diagnostics, surveillance and epidemiology a vast amount of short read data is available, with phylogenetic trees (dendograms) used to visualise the relationships and similarities between samples. Standard reference and assembly based methods can take substantial amounts of time to generate these phylogenetic relationships, with the computation time often exceeding the time to sequence the samples in the first place. Faster methods [@Ondov2016; @Wood2014] can loosely classify samples into known taxonomic categories, however the loss of granularity means the relationships between samples is reduced. This can be the difference between ruling a sample in or out of an outbreak, which is a medically important finding for genomic epidemiologists.
SaffronTree utilises the k-mer profiles between samples to rapidly construct a phylogenetic tree, directly from raw reads in FASTQ or FASTA format. It support NGS data (such as Illumina), 3rd generation long read data (Pacbio/Nanopore) and assembled sequences (FASTA). Firstly, a k-mer count database is constructed for each sample using KMC [@Kokot2017]. Next, the intersection of the k-mer databases is found for each pair of samples, with the number of k-mers in common recorded in a distance matrix. Finally the distance matrix is used to contruct a UPGMA tree [@Sokal1958] in Newick format. The computational complexity of the algorithm is O(N^2), so is best suited to datasets of less than 50 samples. This can give rapid insights into small datasets in minutes, rather than hours. SaffonTree provides better granularity than MLST as it uses more of the underlying genome, can operate at low depth of coverage, is reference free, species agnostic, and has a low memory requirement.

# References