import unittest
import os
import shutil
from saffrontree.SaffronTree import SaffronTree

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','saffrontree')

class Options:
	def __init__(self, output_directory, verbose, threads, kmer, min_kmers_threshold, max_kmers_threshold, input_files):	
		self.output_directory           = output_directory 
		self.verbose                    = verbose
		self.threads                    = threads
		self.kmer                       = kmer
		self.min_kmers_threshold        = min_kmers_threshold
		self.max_kmers_threshold        = max_kmers_threshold
		self.input_files                = input_files

class TestSaffronTree(unittest.TestCase):
	
	'''Do a full run with multiple FASTQ files'''
	def test_fastq_files(self):
		if os.path.exists(os.path.join(data_dir,'out')):
			shutil.rmtree(os.path.join(data_dir,'out'))
			
		options = Options(os.path.join(data_dir,'out'), False, 1, 41, 5, 200, [os.path.join(data_dir,'S_typhi_CT18_chromosome_1.fastq.gz'), os.path.join(data_dir,'S_typhi_CT18_chromosome_2.fastq.gz'),os.path.join(data_dir,'S_typhi_CT18_chromosome_pHCM2_1.fastq.gz'), os.path.join(data_dir,'S_typhi_CT18_chromosome_pHCM2_2.fastq.gz')])
		st = SaffronTree(options)
		self.assertTrue(st.run())
		shutil.rmtree(os.path.join(data_dir,'out'))
		
	'''Mix FASTQ files with FASTA files'''
	def test_fastq_files(self):
		if os.path.exists(os.path.join(data_dir,'out')):
			shutil.rmtree(os.path.join(data_dir,'out'))
			
		options = Options(os.path.join(data_dir,'out'), False, 1, 41, 5, 200, [os.path.join(data_dir,'S_typhi_CT18_chromosome_1.fastq.gz'), os.path.join(data_dir,'S_typhi_CT18_chromosome_2.fastq.gz'), os.path.join(data_dir,'S_typhi_CT18_chromosome.fa')])
		st = SaffronTree(options)
		self.assertTrue(st.run())
		shutil.rmtree(os.path.join(data_dir,'out'))
		