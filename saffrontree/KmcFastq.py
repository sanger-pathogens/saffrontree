import sys
import os
import logging
import subprocess
import tempfile
import shutil

'''Wrapper script around KMC for creating kmer count database from FASTQ files'''
class KmcFastq:
	def __init__(self,output_directory, input_filename, threads, kmer, min_kmers_threshold, max_kmers_threshold):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.input_filename = input_filename
		self.threads = threads
		self.kmer = kmer
		self.min_kmers_threshold = min_kmers_threshold
		self.max_kmers_threshold = max_kmers_threshold
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory))
	
	'''Create tempory output database name'''
	def output_database_name(self):
		return os.path.join(self.temp_working_dir, 'fastq_kmers')
	
	'''Construct the command for the kmc executable'''
	def kmc_command(self):
		return ' '.join(['kmc', '-k'+str(self.kmer), '-ci'+str(self.min_kmers_threshold), '-cx'+str(self.max_kmers_threshold), '-t'+str(self.threads),  self.input_filename, self.output_database_name(), self.temp_working_dir])
	
	'''Run the kmc command'''
	def run(self):	
		self.logger.info("Extracting Kmers from FASTQ file" )
		subprocess.call(self.kmc_command(),shell=True)
	
	'''Cleanup the tempory files'''
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		