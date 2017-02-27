'''Class which represents a single sample (FASTQ file) and associated results'''
class SampleData:
	def __init__(self,fastq_file):
		self.fastq_file = fastq_file
		self.distances = {}
