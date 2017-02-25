import os
 
class SampleData:
	def __init__(self,fastq_file):
		self.fastq_file = fastq_file
		self.basename = self.calculate_basename(fastq_file)
		self.database_name = 'kmc_'+self.basename
		self.distances = {}
	     
	def calculate_basename(self,filename):
		basename = os.path.basename(filename)
		basename = basename.replace('.gz','')
		basename = basename.replace('_1.fastq','')
		return basename
		
	def cleanup(self):
		True
