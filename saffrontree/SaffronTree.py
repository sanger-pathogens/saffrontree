import sys
import os
import logging
import tempfile
import time
import dendropy
from saffrontree.KmcFastq import KmcFastq
from saffrontree.KmcIntersect import KmcIntersect
from saffrontree.SampleData import SampleData
from saffrontree.DistanceMatrix import DistanceMatrix

'''The main driving functionality of the whole application. This takes the input parameters from 
the user and feeds then into different classes to caculate the results. A Newick tree is outputted
at the end.
'''
class SaffronTree:
	def __init__(self,options):
		self.start_time = int(time.time())
		self.logger = logging.getLogger(__name__)
		self.output_directory           = options.output_directory 
		self.verbose                    = options.verbose
		self.threads                    = options.threads
		self.kmer                       = options.kmer
		self.min_kmers_threshold        = options.min_kmers_threshold
		self.max_kmers_threshold        = options.max_kmers_threshold
		self.fastq_files                = options.fastq_files

		if self.verbose:
			self.logger.setLevel(10)

	def run(self):
		os.makedirs(self.output_directory)

		self.logger.info("Generating a kmer database for each sample")
		kmc_samples =[]
		for fastq_file in sorted(self.fastq_files):
			sd = SampleData(fastq_file)
			kmc_fastq = KmcFastq(self.output_directory, fastq_file, self.threads, self.kmer, self.min_kmers_threshold, self.max_kmers_threshold)
			kmc_fastq.run()
			sd.database_name = kmc_fastq.output_database_name()
			kmc_samples.append(sd)
		
		self.logger.info("Generate a database of common kmers")

		largest_count = 1
		for first_sample in kmc_samples:
			for second_sample in kmc_samples:
				if first_sample.fastq_file == second_sample.fastq_file :
					first_sample.distances[first_sample.fastq_file] = 0
					continue
				if second_sample.fastq_file in first_sample.distances:
					continue
				temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(self.output_directory))
				result_database = os.path.join(temp_working_dir, 'fastq_union')
				kmc_intersect = KmcIntersect(first_sample.database_name, second_sample.database_name, self.output_directory, self.threads,result_database)
				kmc_intersect.run()
				first_sample.distances[second_sample.fastq_file] = kmc_intersect.num_common_kmers()
				second_sample.distances[first_sample.fastq_file] = first_sample.distances[second_sample.fastq_file]
				
				if kmc_intersect.common_kmer_count > largest_count:
					largest_count = kmc_intersect.common_kmer_count
					
				kmc_intersect.cleanup()
				
		dm  = DistanceMatrix(self.output_directory,kmc_samples, largest_count)
		dm.create_distance_file()
		pdm = dendropy.PhylogeneticDistanceMatrix.from_csv(
		        src=open(dm.output_distances_file()),
		        delimiter=",")
		tree = pdm.upgma_tree()
		print(tree.as_string("newick"))
			

