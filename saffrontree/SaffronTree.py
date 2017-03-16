import sys
import os
import logging
import tempfile
import time
import dendropy
import shutil
import argparse
from saffrontree.KmcFastq import KmcFastq
from saffrontree.KmcIntersect import KmcIntersect
from saffrontree.SampleData import SampleData
from saffrontree.DistanceMatrix import DistanceMatrix
from saffrontree.KmcVersionDetect import KmcVersionDetect

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
		self.input_files                = options.input_files
		self.keep_files                 = options.keep_files
		self.object_to_be_cleaned       = []
		
		if self.verbose:
			self.logger.setLevel(logging.DEBUG)
		else:
			self.logger.setLevel(logging.ERROR)
		self.kmc_major_version = KmcVersionDetect(self.verbose).major_version()

	def generate_kmers_for_each_file(self):
		kmc_samples =[]
		for input_file in sorted(self.input_files):
			self.logger.warning('Generating kmer counts for %s', input_file)
			sd = SampleData(input_file)
			kmc_fastq = KmcFastq(self.output_directory, input_file, self.threads, self.kmer, self.min_kmers_threshold, self.max_kmers_threshold, self.verbose)
			kmc_fastq.run()
			sd.database_name = kmc_fastq.output_database_name()
			kmc_samples.append(sd)
			self.object_to_be_cleaned.append(kmc_fastq)
		return kmc_samples

	def calculate_intersections_and_largest_count(self, kmc_samples):
		largest_count = 1
		for first_sample in kmc_samples:
			for second_sample in kmc_samples:
				self.logger.warning('Comparing kmers in %s to %s', first_sample.input_file,second_sample.input_file )
				if first_sample.input_file == second_sample.input_file :
					first_sample.distances[first_sample.input_file] = 0
					continue
				if second_sample.input_file in first_sample.distances:
					continue
				temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(self.output_directory),prefix='tmp_pairwisecount_')
				result_database = os.path.join(temp_working_dir, 'fastq_union')
				kmc_intersect = KmcIntersect(first_sample.database_name, second_sample.database_name, self.output_directory, self.threads,result_database, self.verbose, self.kmc_major_version )
				kmc_intersect.run()
				first_sample.distances[second_sample.input_file] = kmc_intersect.num_common_kmers()
				second_sample.distances[first_sample.input_file] = first_sample.distances[second_sample.input_file]
				if not self.verbose:
					shutil.rmtree(temp_working_dir)	
				
				if kmc_intersect.common_kmer_count > largest_count:
					largest_count = kmc_intersect.common_kmer_count
					
				kmc_intersect.cleanup()
		return largest_count

	def create_output_tree(self, kmc_samples, largest_count):
		'''Calculate the tree from the distance matrix'''
		dm  = DistanceMatrix(self.output_directory, kmc_samples, largest_count)
		dm.create_distance_file()
		self.object_to_be_cleaned.append(dm)
		with open(dm.output_distances_file(), 'r') as distance_matrix:
			pdm = dendropy.PhylogeneticDistanceMatrix.from_csv(
		        src=distance_matrix,
		        delimiter=",")
			tree = pdm.upgma_tree()
		
		'''Print the final tree'''
		with open(os.path.join(self.output_directory, 'kmer_tree.newick'), 'w') as tree_file:
			tree_file.write(tree.as_string("newick"))

	def run(self):
		self.logger.warning('Using KMC syntax version %s', self.kmc_major_version)
		os.makedirs(self.output_directory)
		self.logger.warning("Generating a kmer database for each sample")
		kmc_samples = self.generate_kmers_for_each_file()
		
		self.logger.warning("Calculate intersections of kmers between samples")
		largest_count = self.calculate_intersections_and_largest_count(kmc_samples)
		
		self.logger.warning("Creating a newick tree")
		self.create_output_tree(kmc_samples, largest_count)

		if not self.keep_files :
			'''Tidy up all the temp files'''
			for current_obj in self.object_to_be_cleaned:
				current_obj.cleanup()
		return self
			