import os
import logging
import tempfile
import subprocess
import re
 
'''union 2 kmer databases to find common kmers'''
class KmcUnion:
	def __init__(self,first_database, second_database, output_directory, threads,result_database):
		self.logger = logging.getLogger(__name__)
		self.first_database = first_database
		self.second_database = second_database
		self.threads = threads
		self.result_database = result_database
		self.temp_working_dir = tempfile.mkdtemp(dir=output_directory)
		self.kmc_output = ''

	def kmc_union_command(self):
		return ' '.join(['kmc_tools', '-t'+str(self.threads), 'union', self.first_database, self.second_database, self.result_database ])
		
	def kmc_histogram_command(self):
		return ' '.join(['kmc_tools', 'histogram', self.result_database, self.output_histogram_file() ])
	
	def output_histogram_file(self):
		return os.path.join(self.temp_working_dir, 'histogram') 
	
	def run(self):
		self.logger.info("Finding kmers")
		subprocess.call(self.kmc_union_command(),shell=True)
		subprocess.call(self.kmc_histogram_command(),shell=True)
	
	def inverted_num_kmers(self):
		return (1/self.num_common_kmers())
	
	def num_common_kmers(self):
		total = 0
		with open(self.output_histogram_file(), 'r') as histogram_file:
			for line in histogram_file:
			kmer_freq = re.split(r'\t+', line)
			total = total + kmer_freq[1]
		
		return total
	
	def cleanup(self):
		os.remove(self.temp_working_dir)
