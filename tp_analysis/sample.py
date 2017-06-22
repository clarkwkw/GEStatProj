import re
import os

def parse_name(path):
	name = path.split('/')
	name = name[len(name) - 1].split('.')
	name = '.'.join(name[0:(len(name)-1)])
	name = name.split('-')
	if len(name) != 7:
		raise Exception("Invalid sample file: "+path)
	return name

def get_samples(sample_folder):
	try:
		files = os.listdir(sample_folder)
		samples = []
		for file in files:
			file_name = file.split('.')
			if file_name[len(file_name) - 1] == 'txt':
				samples.append(Sample(sample_folder + '/' + file))
		return samples
	except FileNotFoundError:
		print("Folder of samples does not exist, abort.")
		exit(-1)

# [Type]-[Name]-[No]-[think]-[understand]-[language]-[presentation].txt
class Sample:
	def __init__(self, path):
		[self.type, self.name, self.no, self.think, self.understand, self.lang, self.pres] = parse_name(path)

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