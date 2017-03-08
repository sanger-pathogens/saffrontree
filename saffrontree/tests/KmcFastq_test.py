import unittest
import os
from saffrontree.KmcFastq import KmcFastq

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','kmcfastq')

class TestKmcFastq(unittest.TestCase):
	
	'''Check the kmc command and parameters are put together in a sensible manner'''
	def test_kmc_command(self):
		k = KmcFastq(os.getcwd(), os.path.join(data_dir, 'S_typhi_CT18_chromosome_1.fastq.gz'), 1, 10, 10, 200, False  )
		
		# filter out the temp directory
		actual_command = (k.kmc_command()).replace(k.temp_working_dir,'/path')
		actual_command = actual_command.replace(data_dir, '/testdir')
		
		self.assertEqual(actual_command, 'kmc -k10 -fq -ci10 -cx200 -t1 /testdir/S_typhi_CT18_chromosome_1.fastq.gz /path/fastq_kmers /path > /dev/null 2>&1')
		k.cleanup()
		
	'''Dont suppress the KMC output'''
	def test_kmc_command_verbose(self):
		k = KmcFastq(os.getcwd(), os.path.join(data_dir, 'S_typhi_CT18_chromosome_1.fastq.gz'), 1, 10, 10, 200, True  )
		actual_command = (k.kmc_command()).replace(k.temp_working_dir,'/path')
		actual_command = actual_command.replace(data_dir, '/testdir')
		
		self.assertEqual(actual_command, 'kmc -k10 -fq -ci10 -cx200 -t1 /testdir/S_typhi_CT18_chromosome_1.fastq.gz /path/fastq_kmers /path ')
		k.cleanup()
		
		
	'''Check the kmc command and parameters and that min coverage is adjusted to 1'''
	def test_kmc_command_fasta(self):
		k = KmcFastq(os.getcwd(), os.path.join(data_dir, 'sample.fasta'), 1, 10, 10, 200, False  )
		
		# filter out the temp directory
		actual_command = (k.kmc_command()).replace(k.temp_working_dir,'/path')
		actual_command = actual_command.replace(data_dir, '/testdir')
		
		self.assertEqual(actual_command, 'kmc -k10 -fm -ci1 -cx200 -t1 /testdir/sample.fasta /path/fastq_kmers /path > /dev/null 2>&1')
		k.cleanup()
		
	'''When real data is provided, run the kmc command to generate a kmer database'''
	def test_running_kmc_command(self):
		k = KmcFastq(os.getcwd(), os.path.join(data_dir, 'S_typhi_CT18_chromosome_1.fastq.gz'), 1, 10, 10, 200, False )
		self.assertTrue(k.run())
		self.assertTrue(os.path.exists(os.path.join(k.temp_working_dir,'fastq_kmers.kmc_pre')))
		self.assertTrue(os.path.exists(os.path.join(k.temp_working_dir,'fastq_kmers.kmc_suf')))
		
		'''Make sure everything gets cleaned up at the end'''
		k.cleanup()
		self.assertFalse(os.path.exists(k.temp_working_dir))
		