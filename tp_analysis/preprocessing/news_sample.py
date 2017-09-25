import os 
import html
import json
from multiprocessing import Pool as ThreadPool
import random

def get_samples(sample_folder):
	try:
		files = os.listdir(sample_folder)
		files = [sample_folder + "/" + file for file in files]
	except FileNotFoundError:
		print("Folder '%s' does not exist, abort."%sample_folder)
		exit(-1)
	
	return __get_samples_by_paths(files)

def get_samples_multithread(sample_folder, n_thread, random_k = None):
	try:
		files = os.listdir(sample_folder)
		files = [sample_folder + "/" + file for file in files]
	except FileNotFoundError:
		print("Folder '%s' does not exist, abort."%sample_folder)
		exit(-1)

	if type(random_k) is int:
		files = random.sample(files, random_k)

	jobs = []
	start_index, end_index = 0, 0
	for i in range(n_thread):
		start_index = end_index
		end_index = start_index + len(files)//n_thread + (i < len(files)%n_thread)
		jobs.append(files[start_index:end_index])

	pool = ThreadPool()
	tmp_results = pool.map(__get_samples_by_paths, jobs)
	pool.close()
	pool.join()
	result = []
	for tmp_result in tmp_results:
		result.extend(tmp_result) 
	return result

def __get_samples_by_paths(paths):
	samples = []
	for path in paths:
		_, ext = os.path.splitext(path)
		name = os.path.basename(path)
		if ext == '.json' and name != 'master_record.json':
			try:
				samples.append(NewsSample(path))
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
			self.word_count = int(json_dict["wordcount"])
			self.filename = os.path.basename(path)

	def get_identifier(self):
		return self.filename
