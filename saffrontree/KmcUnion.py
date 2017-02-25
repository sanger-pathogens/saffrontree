import os
import logging
import tempfile

from subprocess import check_output
 
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
		
	def run(self):
		self.logger.info("Finding  kmers")
		self.kmc_output = check_output(self.kmc_union_command())
	
	def num_common_kmers(self):
		# parse the kmc_output and extract number of common kmers
		# Do the distances need to be inverted???
		return 1
	
	def cleanup(self):
		os.remove(self.temp_working_dir)
