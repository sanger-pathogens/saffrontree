# SaffronTree
Fast, reference-free pseudo-phylogenomic trees from reads or contigs. 

# Introduction
Quickly build a tree directly from raw reads or from assembled sequences, without the need for a reference sequence or *de novo* assemblies. SaffronTree takes FASTQ/FASTA files as input and uses a kmer analysis to build a phylogenetic neighbour joining tree in newick format.  It works well for small sets of samples (less than 50) but as the algorithm has a complexity of O(N^2), it does not perform well after that point.  This is good enough to give you rapid insights into your data in minutes, rather than hours. During outbreak investigations, researchers and epidemiologies often want to quickly rule a sample in or out of an outbreak. MLST does not provide enough granularity to achieve this, since it is based on only 7 house keeping genes. SaffronTree utilises all of the genomic data in the sample to create a visual representation of the clustering of the data.  It support NGS data (such as Illumina), 3rd generation data (Pacbio/Nanopore) and assembled sequences (FASTA).

[![Build Status](https://travis-ci.org/sanger-pathogens/saffrontree.svg?branch=master)](https://travis-ci.org/sanger-pathogens/saffrontree)

# Usage 
```
usage: saffrontree [options] output_directory *.fastq.gz

SaffronTree: A tool to generate a tree from raw reads, without the need for
references or assembly

positional arguments:
  output_directory      Output directory
  input_files           FASTQ/FASTA files which may be gzipped

optional arguments:
  -h, --help            show this help message and exit
  --kmer KMER, -k KMER  Kmer to use, depends on read length [31]
  --min_kmers_threshold MIN_KMERS_THRESHOLD, -m MIN_KMERS_THRESHOLD
                        Exclude k-mers occurring less than this [5]
  --max_kmers_threshold MAX_KMERS_THRESHOLD, -x MAX_KMERS_THRESHOLD
                        Exclude k-mers occurring more than this [255]
  --threads THREADS, -t THREADS
                        Number of threads [1]
  --keep_files, -f      Keep intermediate files [False]
  --verbose, -v         Turn on more debugging output [False]
  --version             show program's version number and exit
```

## Input parameters
The following parameters change the results:

__kmer__: Choosing a kmer size is not an exact science, and can greatly influence the final results. This kmer size is used by KMC for counting and filtering. It should be an odd number, and a suitable range is between 25-61.  If you choose a kmer too small, you will get too many false positives. If you choose a kmer too big, you will use a lot more RAM and potentially produce insufficient data to construct a tree from. Quite often with Illumina data the beginning and end of the reads have higher sequencing error rates. Ideally you want a kmer size which sits nicely inside the high quality portion of the reads. Quality trimming your reads can help if the quality collapses quite badly at the end of the read.

__min_kmers_threshold__: This value lets you set a minimum threshold for the occurance of a kmer with raw reads. You need about 6x depth to detect a variant with reasonable confidence. Setting this too low will allow random noise (from sequencing errors) through and give you lots of false positives. The maximum suggested value is half the estimated depth of coverage for paired ended data (since forward and reverse reads are evaluated independently). If an input file is in FASTA format, this value is set to 1 for that file, as it assumed it is assembled contigs rather than reads.

__max_kmers_threshold__: This value lets you set a maximum threshold for the occurance of a kmer. With KMC, there is a catchall bin for occurances of 255 and greater (so 255 is the maximum value). By default it is set to 254 which excludes this catchall bin for kmers, and thus the long tail of very common kmers. This reduces the false positives. You need to be careful when setting this too low since you could be excluding interesting kmers.

The following parameters have no impact on the results:

__threads__: This sets the number of threads available to KMC. It should never be more than the number of CPUs available on the server. If you use a compute cluster, make sure to request the same number of threads on a single server. It defaults to 1 and you will get a reasonable speed increase by adding a few CPUs, but the benefit tails off quite rapidly since the I/O becomes the limiting factor (speed of reading files from a disk or network).

__verbose__: By default the output is silent and all intermediate files are deleted as it goes along. Setting this flag allows you output more details of the software as it runs and it keeps the intermediate files.

## Example data
This repository includes some sample data, consisting of FASTQ files and FASTA files derived from Salmonella reference genomes. Only the first 10,000 bases of each reference was taken, however since they all have the same start sites (dnaA) they contain some overlapping material. These sequences were then used to generate simulated reads in FASTQ format.  The data itself covers a variety of serovars of Salmonella (a highly clonal, medically important pathogen). The S. Typhimurium samples would be expected to cluster near each other. Similarly the S. Typhi and S. Paratyphi A would be expected to cluster together. S. Weltevreden is an outgroup and should not be close to any of the other serovars. All of these serovars, except S. Weltevreden, cause very severe disease in Humans.


To build a tree with the FASTA files only:

```
saffrontree output_directory saffrontree/example_data/fastas/*.fa
```
This is the [resulting tree](https://raw.githubusercontent.com/sanger-pathogens/saffrontree/master/saffrontree/example_data/fastas/expected_output_tree.newick). 

To build a tree with the FASTQ files only:
```
saffrontree output_directory saffrontree/example_data/fastqs/*.fastqs.gz
```
This is the [resulting tree](https://raw.githubusercontent.com/sanger-pathogens/saffrontree/master/saffrontree/example_data/fastqs/expected_output_tree.newick).

Finally you can mix FASTAs and FASTQ files (which my be GZipped):
```
saffrontree output_directory saffrontree/example_data/fastas/*.fa saffrontree/example_data/fastqs/*.fastq.gz
```

## Required resources
### RAM (memory)
The RAM(memory) requirement is low, because KMC is extremely efficient and mostly disk based. 

### Disk space
By default all of the intermediate files are cleaned up at the end, so the overall disk space usage is quite low. The intermediate files can be kept if you use the 'verbose' option. 

# Output
A single phylogenetic tree in Newick format is created in the output directory. 

# Installation
There are a number of installation methods. Choosing the right one for the system you use will make life easier. KMC version 2.3+ is supported, with KMC 3+ providing the best performance. 

* Linux/OSX/Windows/Cloud
  * Docker
* Linux 
  * Debian Testing/Ubuntu 16.04 (Xenial)
  * Linuxbrew
* OSX
  * HomeBrew
  * OSX manual method

# Linux/OSX/Windows/Cloud
## Docker 
Install [Docker](https://www.docker.com/).  We have a docker container which gets automatically built from the latest version of SaffronTree. To install it:

```
docker pull sangerpathogens/saffrontree
```

To use it you would use a command such as this (substituting in your directories), where your files are assumed to be stored in /home/ubuntu/data:
```
docker run --rm -it -v /home/ubuntu/data:/data sangerpathogens/saffrontree saffrontree output sample1.fastq.gz sample2.fastq.gz
```

To run some of the example data that is part the repository run:
```
docker run --rm -it -v /home/ubuntu/data:/data sangerpathogens/saffrontree saffrontree output_directory /usr/local/lib/python3.5/dist-packages/saffrontree/example_data/fastqs/start_Salmonella_enterica_subsp_enterica_serovar_Typhi_Ty2_v1_1.fastq.gz /usr/local/lib/python3.5/dist-packages/saffrontree/example_data/fastqs/start_Salmonella_enterica_subsp_enterica_serovar_Typhimurium_SL1344_v4_1.fastq.gz
```

You will then have a tree in:
```
/home/ubuntu/data/output_directory/kmer_tree.newick
```

## Linux
The instructions for Linux assume you have root (sudo) on your machine. 

### Debian Testing/Ubuntu 16.04 (Xenial)
```
apt-get update -qq
apt-get install -y git python3 python3-setuptools python3-biopython python3-pip kmc
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

### Linuxbrew
First install [LinuxBrew](http://linuxbrew.sh/), then follow the instructions below.

```
brew tap homebrew/science
brew update
brew install python3 kmc spades
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

## OSX

### Homebrew
First install [HomeBrew](http://brew.sh/), then follow the instructions below.

```
brew tap homebrew/science
brew update
brew install python3 kmc spades
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

### OSX manual method
Ensure Python 3.5+ is available or install it from https://www.python.org/downloads/ then follow the instructions below:
```
wget https://github.com/refresh-bio/KMC/releases/download/v3.0.0/KMC3.mac.tar.gz 
tar zxf KMC3.mac.tar.gz
export PATH=$PWD:$PATH
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

# FAQ
## How to contribute to the software
If you wish to contribute to this software please fork the project on GitHub and submit a pull request. We will endevor to review it within a few days. Please include automated tests and example data (if relevant) in your pull request and ensure all the existing tests already pass. Comments and documentation should be in British English.

## Bug reports, feature requests and any questions
If you wish to report a bug, request a new feature or have any queries about how the software works, please submit an issue on the GitHub repository page. We will try to fix bugs in a timely fashion. New feature requests will depend on if we find them useful in our own work. If you would like to contact us directly, you can email path-help@sanger.ac.uk and we will get back to you. We are based in the UK (GMT), working Monday to Friday (9-5).

## I found a bug with some data but its private, can I send it to you for debugging?
Please do not send us any private data. We will not sign an NDA. 

## Arent distance matrix based trees inherently phenetic?
It depends on who you talk to. Yes they have less power than more modern methods which reconstruct the ancestory, however if you have a small amount of raw data you can get an answer faster.

## Why UPGMA trees?
Its fast, its implemented already in python, so installation is trivial, and it doesnt give you negative branch lengths like neigbour joining.

## Can I use long read data?
If your PacBio/nanopore (long read) data is in FASTQ format, then the answer is yes, however we have only tested it on corrected reads. Uncorrected reads are unlikely to work because your nearly guaranteed that a sequencing error will occur inside of the length of a k-mer.

## Will you make it work with Python 2?
No. Python 3 is well supported, stable and mature, so please just install this instead.

## Will there be a Windows version?
The only way to run it on Windows is via Docker. We have no plans for a native version. Honestly though, if your using Windows to perform bioinformatics, your in trouble.

## How do I view Newick trees?
The newick format is widely supported and I find [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) to be excellent.

## Do you plan to support other formats like Nexsus?
No, we have no plans to support other tree types, since Newick does the job.

## Its really slow on massive datasets
Yes, the complexity is O(N^2), which means it scales poorly. But for a few dozen samples it works much quicker than other methods, so it fills a niche.

## What method is used for tree construction?
We use UPGMA, which is like Neighbour Joining.

## Can I send you my data for analysis?
No, please install the software yourself and perform your own analysis.

## The branch lengths are crazy?
Its a quick and dirty analysis from raw reads, so accuratly estimating branch lengths can be difficult. Whats important is what samples are near each other on a tree.

## Do I need to provide both forward and reverse reads?
No, all FASTQ files are treated independantly, so they will end up in the same place in the tree (if everything goes to plan).

## Can I mix FASTA and FASTQ files?
Yes.

## Can the input files be GZipped?
Yes, it automatically uncompresses them on the fly. You can mix and match compressed and uncompressed files.
