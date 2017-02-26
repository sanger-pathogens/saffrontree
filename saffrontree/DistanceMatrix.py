import sys
import os
import logging
import subprocess
import tempfile
import shutil
import math

class DistanceMatrix:
	def __init__(self,output_directory, samples,smallest_count):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.samples = samples
		self.smallest_count = smallest_count
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory))
	
	def output_distances_file(self):
		return os.path.join(self.temp_working_dir, 'distances.csv')
	
	def adjust_distance(self, distance):
		offset_distance = distance - self.smallest_count
		if offset_distance > 0:
			offset_distance = 1/math.log1p(offset_distance)
		return offset_distance
	
	def create_distance_file(self):
		with open(self.output_distances_file(), 'w') as file_of_distances:
			
			# header 
			file_of_distances.write(',')
			file_of_distances.write( ','.join(sorted(self.samples[0].distances.keys())) + "\n")
			
			for sample in self.samples:
				file_of_distances.write(sample.fastq_file + ',')
				distances = []
				for filename in sorted(sample.distances.keys()):
					distances.append(str(self.adjust_distance(sample.distances[filename])))
				file_of_distances.write( ','.join(distances) + "\n")
	
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		