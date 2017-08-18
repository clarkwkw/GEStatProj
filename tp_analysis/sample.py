import re
import os

def parse_name(path):
	name = os.path.basename(path)
	name, _ = os.path.splitext(name)
	name = name.split('-')
	if len(name) != 7 and len(name) != 8:
		raise Exception("Invalid sample file: "+path)
	return name

def get_samples(sample_folder):
	try:
		files = os.listdir(sample_folder)
		samples = []
		for file in files:
			_, ext = os.path.splitext(file)
			if ext == '.txt':
				samples.append(Sample(sample_folder + '/' + file))
		return samples
	except FileNotFoundError:
		print("Folder of samples does not exist, abort.")
		exit(-1)

def partition(samples, folds = 10, index_only = False):
	if folds < 1 or folds > len(samples):
		raise Exception("'folds' must be between 1 and len(sample)")
	start, end = (0, 0)
	for i in range(folds):
		start = end
		end += (len(samples) - end)//(folds - i)
		if index_only:
			yield (start, end)
		else:
			yield samples[start:end]

# [Type]-[Name]-[No](-[Question No.])-[think]-[understand]-[language]-[presentation].txt
class Sample:
	def __init__(self, path):
		result = parse_name(path)
		if len(result) == 7:
			[self.type, self.name, self.no, self.think, self.understand, self.lang, self.pres] = result
			self.question = None
		else:
			[self.type, self.name, self.no, self.question, self.think, self.understand, self.lang, self.pres] = result

		self.think = float(self.think)
		self.understand = float(self.understand)
		self.lang = float(self.lang)
		self.pres = float(self.pres)

		file = open(path, "r")
		self.text = file.readlines()
		self.text = '\n'.join(self.text)
		file.close()

	def get_identifier(self):
		return self.type+'-'+self.name+'-'+self.no