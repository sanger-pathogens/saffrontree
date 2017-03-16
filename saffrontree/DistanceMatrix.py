import sys
import os
import subprocess
import tempfile
import shutil
import math

'''Take in the results of the kmer analysis and create distance matrix that can be used to build a tree.'''
class DistanceMatrix:
	def __init__(self,output_directory, samples,largest_count):
		self.output_directory = output_directory
		self.samples = samples
		self.largest_count = largest_count
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory), prefix='tmp_distancematrix_')
	
	'''The name of the file containing the matrix of distances'''
	def output_distances_file(self):
		return os.path.join(self.temp_working_dir, 'distances.csv')
	
	'''The tree building algorithms put things with the shortest distance near each other'''
	'''however our raw data is the opposite (num kmers in common), so we subtract from the larget distance found.'''
	def adjust_distance(self, distance):
		if distance == 0:
			return 0
		offset_distance = (self.largest_count + 1) - (distance)
		if offset_distance > 0:
			return offset_distance
		else:
			return 0
	
	'''Create a tempory file containing the distances matrix.The samples in the header and row 1 have to be sorted identically.'''
	'''This is what the finished file looks like (minus spacing).
			       ,sample1,sample2,sample3
			sample1,      0,      5,      9
			sample2,      5,      0,      6
			sample3,      9,      6,      0
	'''
	def create_distance_file(self):
		with open(self.output_distances_file(), 'w') as file_of_distances:
			
			'''Create the header, consisting of sorted filenames'''
			file_of_distances.write(',')
			file_of_distances.write( ','.join(sorted(self.samples[0].distances.keys())) + "\n")
			
			'''Sort the filenames in the same order as header'''
			for sample in sorted(self.samples, key=lambda x: x.input_file) :
				file_of_distances.write(sample.input_file + ',')
				
				'''lookup the distances for this sample against all others'''
				distances = []
				for filename in sorted(sample.distances.keys()):
					distances.append(str(self.adjust_distance(sample.distances[filename]) ) )
				file_of_distances.write( ','.join(distances) + "\n")
	
	'''Delete the temp files when no longer needed'''
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		