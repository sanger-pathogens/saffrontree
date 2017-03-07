#SaffronTree
Quickly build a tree directly from raw reads or from assembled sequences, without the need for a reference sequence or de novo assemblies. SaffronTree takes FASTQ/FASTA files as input and uses a kmer analysis to build a phylogenetic neighbour joining tree in newick format.  It works well for small sets of samples (less than 50) but as the algorithm has a complexity of O(N^2), it does not perform well after that point.  This is good enough to give you rapid insights into your data in minutes, rather than hours. During outbreak investigations, researchers and epidemiologies often want to quickly rule a sample in or out of an outbreak. MLST does not provide enough granularity to achieve this, since it is based on only 7 house keeping genes. SaffronTree utilises all of the genomic data in the sample to create a visual representation of the clustering of the data.  It support NGS data (such as Illumina), 3rd generation data (Pacbio/Nanopore) and assembled sequences (FASTA).

[![Build Status](https://travis-ci.org/sanger-pathogens/saffrontree.svg?branch=master)](https://travis-ci.org/sanger-pathogens/saffrontree)

#Usage 
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
  --verbose, -v         Turn on debugging [0]
  --version             show program's version number and exit
```

##Input parameters
The following parameters change the results:

__kmer__: Choosing a kmer is not an exact science, and have greatly influence the final results. This kmer size is used by KMC for counting and filtering.  It should be an odd number and a common range is between 25-61.  If choose a kmer which is too small, you will get a lot more false positives. If you choose a kmer too big, you will use a lot more RAM and potentially get too little data returned. Quite often with Illumina data the beginning and end of the reads have higher sequencing error rates. Ideally you want a kmer size which sits nicely inside the good cycles of the reads. Trimming with Trimmomatic can help if the quality collapses quite badly at the end of the read.

__min_kmers_threshold__: This value lets you set a minimum threshold for the occurance of a kmer with raw reads. You need about 6X to detect if a variant is present with reasonable confidence. Setting this too low will allow random noise through and give you lots of false positives. The maximum suggested value is half the estimated depth of coverage for paired ended data ( since forward and reverse reads are evaluated independantly).  If an input file is in FASTA format, this value is set to 1 for that file.

__max_kmers_threshold__: This value lets you set a maximum threshold for the occurance of a kmer. With KMC, there is a catchall bin for occurances of 255 and greater (so 255 is the maximum value). By default it is set to 254 which excludes this catchall bin for kmers, and thus the long tail of very common kmers. This reduces the false positives. You need to be careful when setting this too low since you could be excluding interesting kmers.

The following parameters have no impact on the results:

__threads__: This sets the number of threads available to KMC. It should never be more than the number of CPUs available on the server. If you use a compute cluster, make sure to request the same number of threads on a single server. It defaults to 1 and you will get a reasonable speed increase by adding a few CPUs, but the benefit tails off quite rapidly since the I/O becomes the limiting factor (speed of reading files from a disk or network).

__verbose__: By default the output is silent and all intermediate files are deleted as it goes along. Setting this flag allows you output more details of the software as it runs and it keeps the intermediate files.

##Required resources
###RAM (memory)
The RAM(memory) requirement is low, because KMC is extremely efficient and mostly disk based. 

###Disk space
By default all of the intermediate files are cleaned up at the end, so the overall disk space usage is quite low. The intermediate files can be kept if you use the 'verbose' option. 

#Output
A single phylogenetic tree in Newick format is created in the output directory. 

#Installation
There are a number of installation methods. Choosing the right one for the system you use will make life easier. As KMC version 3 is not currently packaged for any system (only the incompatible version 2.3.0), you will need to manually install it, and should add it permanently to your PATH.

* Linux 
  * Debian Testing/Ubuntu 16.04 (Xenial)
  * Manual Linux
* OSX
* Linux/OSX/Windows/Cloud
  * Docker

##Linux
The instructions for Linux assume you have root (sudo) on your machine. 

###Debian Testing/Ubuntu 16.04 (Xenial)
```
apt-get update -qq
apt-get install -y wget git python3 python3-setuptools python3-biopython python3-pip
mkdir -p bin
cd bin
wget https://github.com/refresh-bio/KMC/releases/download/v3.0.0/KMC3.linux.tar.gz 
tar zxf KMC3.linux.tar.gz
export PATH=$PWD:$PATH
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

###Manual Linux
Ensure Python 3.5+ is available or install it from https://www.python.org/downloads/ then follow the instructions below:
```
wget https://github.com/refresh-bio/KMC/releases/download/v3.0.0/KMC3.linux.tar.gz 
tar zxf KMC3.linux.tar.gz
export PATH=$PWD:$PATH
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

##OSX
Ensure Python 3.5+ is available or install it from https://www.python.org/downloads/ then follow the instructions below:
```
wget https://github.com/refresh-bio/KMC/releases/download/v3.0.0/KMC3.mac.tar.gz 
tar zxf KMC3.mac.tar.gz
export PATH=$PWD:$PATH
pip3 install git+git://github.com/sanger-pathogens/saffrontree.git
```

#Linux/OSX/Windows/Cloud
##Docker 
Install [Docker](https://www.docker.com/).  We have a docker container which gets automatically built from the latest version of SaffronTree. To install it:

```
docker pull sangerpathogens/saffrontree
```

To use it you would use a command such as this (substituting in your directories), where your files are assumed to be stored in /home/ubuntu/data:
```
docker run --rm -it -v /home/ubuntu/data:/data sangerpathogens/saffrontree saffrontree output sample1.fastq.gz sample2.fastq.gz
```
To run the example data that is part the repository run:
```
docker run --rm -it -v /home/ubuntu/data:/data sangerpathogens/saffrontree saffrontree output /usr/local/lib/python3.5/dist-packages/saffrontree/example_data/*
```

