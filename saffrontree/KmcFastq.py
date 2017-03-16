import sys
import os
import re
import logging
import subprocess
import tempfile
import shutil

'''Wrapper script around KMC for creating kmer count database from FASTQ files'''
class KmcFastq:
	def __init__(self,output_directory, input_filename, threads, kmer, min_kmers_threshold, max_kmers_threshold, verbose):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.input_filename = input_filename
		self.threads = threads
		self.kmer = kmer
		
		if self.file_type_option() == '-fm':
			# a FASTA file doesnt have a depth of coverage
			self.min_kmers_threshold = 1
		else:
			self.min_kmers_threshold = min_kmers_threshold
			
		self.max_kmers_threshold = max_kmers_threshold
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory),prefix='tmp_samplekmers_')
		self.verbose = verbose
		if self.verbose:
			self.logger.setLevel(logging.DEBUG)
		else:
			self.logger.setLevel(logging.ERROR)
	
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
		redirect_output = ''
		if self.verbose:
			redirect_output = ''
		else:
			redirect_output = '> /dev/null 2>&1'
		
		command_to_run = ' '.join(['kmc', '-k'+str(self.kmer), self.file_type_option(), '-ci'+str(self.min_kmers_threshold), '-cx'+str(self.max_kmers_threshold), '-t'+str(self.threads),  self.input_filename, self.output_database_name(), self.temp_working_dir, redirect_output])
		self.logger.warning("Running: "+command_to_run )
		return command_to_run
	
	'''Run the kmc command'''
	def run(self):	
		self.logger.warning("Extracting Kmers from FASTQ file" )
		subprocess.call(self.kmc_command(),shell=True)
		return self
	
	'''Cleanup the tempory files'''
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		