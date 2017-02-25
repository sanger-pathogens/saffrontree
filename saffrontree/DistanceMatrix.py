import sys
import os
import logging
import subprocess
import tempfile
import shutil

class DistanceMatrix:
	def __init__(self,output_directory, samples):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.samples = samples
		self.temp_working_dir = tempfile.mkdtemp(dir=os.path.abspath(output_directory))
	
	def output_distances_file(self):
		return os.path.join(self.temp_working_dir, 'distances.csv')
	
	def create_distance_file(self):
		with open(self.output_distances_file(), 'w') as file_of_distances:
			
			# header 
			file_of_distances.write(',')
			file_of_distances.write( ','.join(keys(sorted(self.samples[0].distances))) + "\n")
			file_of_distances.write( ','.join(self.samples[0].distances.keys().sorted()) + "\n")
			
			for sample in self.samples:
				file_of_distances.write(sample.fastq_file + ',')
				distances = []
				for filename in sample.distances.keys().sorted()
					distance.append(sample.distances[filename])
				file_of_distances.write( ','.join(distance) + "\n")
	
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)	
		