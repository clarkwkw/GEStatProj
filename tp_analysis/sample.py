import re

def parse_name(path):
	name = path.split('/')
	name = name[len(name) - 1].split('.')
	name = '.'.join(name[0:(len(name)-1)])
	name = name.split('-')
	if len(name) != 6:
		raise Exception("Invalid sample path: "+path)
	return name

class Sample:
	def __init__(self, path):
		[self.name, self.no, self.think, self.understand, self.lang, self.pres] = parse_name(path)

		self.name = self.name+'-'+self.no
		self.think = float(self.think)
		self.understand = float(self.understand)
		self.lang = float(self.lang)
		self.pres = float(self.pres)

		file = open(path, "r")
		self.text = file.readlines()
		self.text = '\n'.join(self.text)
		file.close()