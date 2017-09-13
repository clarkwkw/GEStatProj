import os 
import html
import json

def get_samples(sample_folder):
	try:
		files = os.listdir(sample_folder)
	except FileNotFoundError:
		print("Folder '%s' does not exist, abort."%sample_folder)
		exit(-1)
	samples = []
	for file in files:
		_, ext = os.path.splitext(file)
		name = os.path.basename(file)
		if ext == '.json' and name != 'master_record.json':
			try:
				samples.append(NewsSample(sample_folder + '/' + file))
			except:
				print("Cannot read news sample %s"%name)
	return samples
	

class NewsSample:
	def __init__(self, path):
		with open(path, "r") as f:
			json_dict = json.load(f, strict = False)
			self.headline = json_dict["headline"]
			self.text = html.unescape(json_dict["text"])
			self.section = json_dict["section"]
			self.id = None
			if "gid" in json_dict:
				self.id = json_dict["gid"]
			self.wordcount = int(json_dict["wordcount"])
			self.filename = os.path.basename(path)

	def get_identifier(self):
		return self.filename
