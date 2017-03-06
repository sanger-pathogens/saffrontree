'''Class which represents a single sample (FASTQ file) and associated results'''
class SampleData:
	def __init__(self,input_file):
		self.input_file = input_file
		self.distances = {}
