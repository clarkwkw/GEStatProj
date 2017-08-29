import re
import os
import json

def get_samples(sample_folder):
	try:
		files = os.listdir(sample_folder)
		samples = []
		for file in files:
			_, ext = os.path.splitext(file)
			if ext == '.json':
				samples.append(TPSample(sample_folder + '/' + file))
		return samples
	except FileNotFoundError:
		print("Folder '%s' does not exist, abort."%sample_folder)
		exit(-1)

class TPSample:
	def __init__(self, path):
		with open(path, "r") as f:
			json_dict = json.load(f)

		self.type = json_dict["type"]
		self.batch_name = json_dict["batch_name"]
		self.batch_no = json_dict["batch_no"]

		self.question = json_dict["question"]

		self.think = json_dict["score"]["think"]
		self.understand = json_dict["score"]["understand"]
		self.lang = json_dict["score"]["lang"]
		self.pres = json_dict["score"]["pres"]

		self.text = json_dict["text"].encode("ascii", "ignore")

		if "comment" in json_dict:
			self.comment = json_dict["comment"]
		else:
			self.comment = ""
		
	def get_identifier(self):
		return self.type+'-'+self.batch_name+'-'+self.batch_no