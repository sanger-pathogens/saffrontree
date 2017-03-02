import unittest
import os
from saffrontree.DistanceMatrix import DistanceMatrix
from saffrontree.SampleData import SampleData

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','distancematrix')

class TestDistanceMatrix(unittest.TestCase):
	
	'''Given a list of distances, subtract them from the largest'''
	def test_adjust_distances(self):
		s1 = SampleData('sample1.fastq')
		s2 = SampleData('sample2.fastq')
		s1.distances = {'sample2.fastq': 123,'sample1.fastq': 0}
		s2.distances = {'sample2.fastq': 0,'sample1.fastq': 143}
		
		d = DistanceMatrix( os.getcwd(),[s1,s2], 500 )
		self.assertEqual(d.adjust_distance(100),401)
		self.assertEqual(d.adjust_distance(0),0)
		d.cleanup()
		
	'''Dendropy needs a csv file of the matrix of distances with the filenames as 1st row and col'''
	def test_create_distance_file(self):
		s1 = SampleData('sample1.fastq')
		s2 = SampleData('sample2.fastq')
		s3 = SampleData('sample3.fastq')
		s1.distances = {'sample1.fastq': 0, 'sample2.fastq': 5, 'sample3.fastq': 6}
		s2.distances = {'sample1.fastq': 5, 'sample2.fastq': 0, 'sample3.fastq': 3}
		s3.distances = {'sample1.fastq': 6, 'sample2.fastq': 3, 'sample3.fastq': 0}
		
		d = DistanceMatrix( os.getcwd(),[s1, s2, s3], 6)
		d.create_distance_file()
		self.assertTrue(os.path.exists(d.output_distances_file()))
		
		with open(d.output_distances_file(), 'r') as actual_file, open(os.path.join(data_dir, 'expected_distance_matrix.csv'), 'r') as expected_file:
			actual_config_content = actual_file.read()
			expected_config_content = expected_file.read()
			
			self.assertEqual(actual_config_content,expected_config_content)
		d.cleanup()