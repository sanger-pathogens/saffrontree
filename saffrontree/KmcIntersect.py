import os
import logging
import tempfile
import subprocess
import shutil
import re
 
'''Wrapper around KMC tools to intersect 2 kmer databases to find common kmers'''
class KmcIntersect:
	def __init__(self,first_database, second_database, output_directory, threads, result_database, verbose = False):
		self.logger = logging.getLogger(__name__)
		self.first_database = first_database
		self.second_database = second_database
		self.threads = threads
		self.result_database = result_database
		self.temp_working_dir = tempfile.mkdtemp(dir=output_directory)
		self.kmc_output = ''
		self.common_kmer_count = 0
		self.verbose = verbose

	'''Construct the command for kmc_tools to find the intersection of two databases'''
	def kmc_intersect_command(self):
		redirect_output = '> /dev/null 2>&1'
		if self.verbose:
			redirect_output = ''
		return ' '.join(['kmc_tools', '-t'+str(self.threads), 'simple', self.first_database, self.second_database, 'intersect', self.result_database, redirect_output ])
	
	'''Construct the command for kmc_tools to generate a histogram of the kmer frequencies'''	
	def kmc_histogram_command(self):
		redirect_output = '> /dev/null 2>&1'
		if self.verbose:
			redirect_output = ''
		return ' '.join(['kmc_tools', 'transform', self.result_database, 'histogram',  self.output_histogram_file(), redirect_output ])
	
	'''The temp filename of the histogram output'''
	def output_histogram_file(self):
		return os.path.join(self.temp_working_dir, 'histogram') 
	
	'''Find the intersection of the two databases, and count number of kmers in common'''
	def run(self):
		self.logger.info("Finding kmers")
		subprocess.call(self.kmc_intersect_command(), shell=True)
		subprocess.call(self.kmc_histogram_command(), shell=True)
		self.common_kmer_count = self.num_common_kmers()
		return self
	
	'''From the output of the histogram frequency count, calculate the number of kmers in common'''
	def num_common_kmers(self):
		total = 0
		if not os.path.exists(self.output_histogram_file()):
			return 1

		'''The histogram file has the no. of times kmer occurs in the first column and the 2nd column has the frequency. An example of the histogram file is'''
		'''
		5	123
		6	444
		7	567
		8	99999
		9	12
		'''
		with open(self.output_histogram_file(), 'r') as histogram_file:
			for line in histogram_file:
				kmer_freq = re.split(r'\t+', line)
				total = total + int(kmer_freq[1])
		
		return total
	
	'''Cleanup the tempory files'''
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)
