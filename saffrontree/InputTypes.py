import os
import argparse

'''Methods to validate the input parameters passed in by the user'''
class InputTypes:
	
	'''Check the output directory doesnt already exist to avoid overwriting previous results'''
	def is_output_directory_valid(filename):
		if os.path.exists(filename):
			raise argparse.ArgumentTypeError("The output directory already exists")
		return filename
	
	'''All of the input files listed should exist'''
	def is_fastq_valid(filename):
		if not os.path.exists(filename):
			raise argparse.ArgumentTypeError('Cannot access input file')
		return filename
	
	'''Has a sensible kmer been passed in'''
	def is_kmer_valid(value_str):
		if value_str.isdigit():
			kmer = int(value_str)
			if kmer%2 == 1 and kmer >= 21 and kmer <= 255:
				return kmer
		raise argparse.ArgumentTypeError("Invalid Kmer value, it must be an odd integer between 21 and 255")
	
	'''Check that the minimum threshold for kmer counts is in a range KMC can use'''
	def is_min_kmers_threshold_valid(value_str):
		if value_str.isdigit():
			min_kmers_threshold = int(value_str)
			if  min_kmers_threshold >= 0 and min_kmers_threshold <= 255:
				return min_kmers_threshold
		raise argparse.ArgumentTypeError("Invalid minimum kmers threshold, it must be between 0 and 255, but ideally less than half the mean coverage.")

	'''Check that the maximum threshold for kmer counts is in a range KMC can use'''
	def is_max_kmers_threshold_valid(value_str):
		if value_str.isdigit():
			max_kmers_threshold = int(value_str)
			if  max_kmers_threshold >= 10 and max_kmers_threshold <= 255:
				return max_kmers_threshold
		raise argparse.ArgumentTypeError("Invalid maximum kmers threshold, it must be between 10 and 255, and greater than the minimum kmer value, but ideally greater than the coverage.")
		
	'''Check the number of threads is sensible, for use with KMC'''
	def is_threads_valid(value_str):
		if value_str.isdigit():
			threads = int(value_str)
			if  threads > 0 and threads <= 1024:
				return threads
		raise argparse.ArgumentTypeError("Invalid number of threads, it must at least 1 and less than the No. of CPUs")
		