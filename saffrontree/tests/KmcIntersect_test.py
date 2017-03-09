import unittest
import os
from saffrontree.KmcIntersect import KmcIntersect
from saffrontree.KmcFastq import KmcFastq

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','kmcintersect')

class TestKmcIntersect(unittest.TestCase):
	
	'''Check the intersect command and parameters are put together in a sensible manner'''
	def test_kmc_intersect_command(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', False, 3 )
		
		self.assertEqual(k.kmc_intersect_command(), 'kmc_tools -t1 simple first_database second_database intersect results > /dev/null 2>&1')
		k.cleanup()
		
	'''Check the intersect command for kmc version 2'''
	def test_kmc_intersect_command_kmc2(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', False, 2 )
		
		self.assertEqual(k.kmc_intersect_command(), 'kmc_tools -t1 intersect first_database second_database results > /dev/null 2>&1')
		k.cleanup()
		
	'''Dont suppress the KMC tools output'''
	def test_kmc_intersect_command_verbose(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', True, 3 )
		
		self.assertEqual(k.kmc_intersect_command(), 'kmc_tools -t1 simple first_database second_database intersect results ')
		k.cleanup()

	'''check the histogram command is correctly constructed'''
	def test_kmc_histogram_command(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', False, 3 )
		
		actual_command = (k.kmc_histogram_command()).replace(k.temp_working_dir,'/path')
		self.assertEqual(actual_command, 'kmc_tools transform results histogram /path/histogram > /dev/null 2>&1')	
		k.cleanup()
		
	'''check the histogram command for kmc 2'''
	def test_kmc_histogram_command_kmc2(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', False, 2 )
		
		actual_command = (k.kmc_histogram_command()).replace(k.temp_working_dir,'/path')
		self.assertEqual(actual_command, 'kmc_tools histogram results /path/histogram > /dev/null 2>&1')	
		k.cleanup()
		
	'''check the histogram command can be verbose'''
	def test_kmc_histogram_command_verbose(self):
		k = KmcIntersect('first_database','second_database', os.getcwd(), 1, 'results', True, 3 )
		
		actual_command = (k.kmc_histogram_command()).replace(k.temp_working_dir,'/path')
		self.assertEqual(actual_command, 'kmc_tools transform results histogram /path/histogram ')
		k.cleanup()

	def test_running_intersection_and_counting_kmers(self):
		first_sample = KmcFastq(os.getcwd(), os.path.join(data_dir, 'S_typhi_CT18_chromosome_1.fastq.gz'), 1, 10, 10, 200, False )
		first_db = first_sample.run().output_database_name()
		second_sample = KmcFastq(os.getcwd(), os.path.join(data_dir, 'S_typhi_CT18_chromosome_1.fastq.gz'), 1, 10, 10, 200, False )
		second_db = second_sample.run().output_database_name()
		k = KmcIntersect(first_db,second_db, os.getcwd(), 1, 'results', False, 3 )
		
		self.assertTrue(k.run())
		self.assertTrue(os.path.exists('results.kmc_pre'))
		self.assertTrue(os.path.exists('results.kmc_suf'))
		self.assertTrue(os.path.exists(k.output_histogram_file()))
		self.assertEqual(k.common_kmer_count, 5569)
		
		'''Make sure everything gets cleaned up at the end'''
		k.cleanup()
		self.assertFalse(os.path.exists(k.temp_working_dir))
		first_sample.cleanup()
		second_sample.cleanup()
		os.remove('results.kmc_pre')
		os.remove('results.kmc_suf')
		