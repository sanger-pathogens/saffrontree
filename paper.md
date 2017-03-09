---
title: 'SaffronTree: Reference free rapid phylogenetic tree construction from raw read data'
tags:
  - bioinformatics
  - phylogenetics
  - bacteria
authors:
 - name: Andrew J. Page
   orcid: 0000-0001-6919-6062
   affiliation: Pathogen Informatics, Wellcome Trust Sanger Institute
 - name: Martin G. Hunt
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
When defining bacterial populations through whole genome sequencing (WGS) the samples often have unknown evolutionary histories.  With the increased use of next generation WGS in routine diagnostics, surveillance and epidemiology a vast amount of short read data is available, with phylogenetic trees (dendograms) used to visualise the relationships and similariies betweeen samples. Existing reference and assembly based methods can take stubstantial amounts of time to generate these phylogenetic relationships, with the computation time often exceeding the time to sequence the sample in the first place. Faster methods [MASH, kraken] can  loosely classify samples into known taxonomic categories, however the loss of grandularity means the relationships between samples is reduced. This can be the difference between ruling an sample in or out of an outbreak, which is a medically important finding for genomic epidimoglists.
SaffronTree utilises the k-mer profiles between samples to rapidly construct a phylogenetic tree, directly from raw reads in FASTQ or FASTA format. It support NGS data (such as Illumina), 3rd generation long read data (Pacbio/Nanopore) and assembled sequences (FASTA). A UPGMA tree [ref] is constructed in Newick format. The computational complexity is O(N^2), so is best suited to datasets of less than 50 samples. This is good enough to give you rapid insights into datasets in minutes, rather than hours. After this point it becomes more efficient to use other methods, such as de novo assemblies, with pan genome construction [ref roary] and maximum likelihood tree construction algorithms [ref raxml]. SaffonTree provides better granularity than MLST, is reference free, species agnostic, and has a low memory requirement.


# References