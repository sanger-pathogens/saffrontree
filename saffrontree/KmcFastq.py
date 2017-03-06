import sys
import os
import re
import logging
import subprocess
import tempfile
import shutil

'''Wrapper script around KMC for creating kmer count database from FASTQ files'''
class KmcFastq:
	def __init__(self,output_directory, input_filename, threads, kmer, min_kmers_threshold, max_kmers_threshold, verbose = False):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.input_filename = input_filename
		self.threads = threads
		self.kmer = kmer
		self.min_kmers_threshold = min_kmers_threshold
		self.max_kmers_threshold = max_kmers_threshold
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory))
		self.verbose = verbose
	
	'''Create tempory output database name'''
	def output_database_name(self):
		return os.path.join(self.temp_working_dir, 'fastq_kmers')
	
	'''A FASTA file needs a different option for KMC'''
	def file_type_option(self):
		m = re.search('\.(fasta|fa|fsa|fna)(.gz)?$', self.input_filename)
		if m and m.group(0):
			return '-fm'
		else:
			return '-fq'
	
	'''Construct the command for the kmc executable'''
	def kmc_command(self):
		redirect_output = '> /dev/null 2>&1'
		if self.verbose:
			redirect_output = ''
		return ' '.join(['kmc', '-k'+str(self.kmer), self.file_type_option(), '-ci'+str(self.min_kmers_threshold), '-cx'+str(self.max_kmers_threshold), '-t'+str(self.threads),  self.input_filename, self.output_database_name(), self.temp_working_dir, redirect_output])
	
	'''Run the kmc command'''
	def run(self):	
		self.logger.info("Extracting Kmers from FASTQ file" )
		subprocess.call(self.kmc_command(),shell=True)
		return self
	
	'''Cleanup the tempory files'''
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		