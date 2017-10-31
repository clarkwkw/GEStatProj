import json
import models
import numpy as np
import os
import preprocessing
import random
import tensorflow as tf
import pandas

_essay_folder = "./samples"
_model = "./output/NN"
_type = "NN"
_grouped_sections = ['education', 'science & technology', 'environment', 'global-development', 'business']
_words = []
_norm_dict = None
pca_components = None
model = None

with open(_model+"/preprocess.json", "r") as f:
	preprocess_dict = json.load(f)
	_words = preprocess_dict["words"]
	if "norm_info" in preprocess_dict:
		_norm_dict = preprocess_dict["norm_info"]
	if preprocess_dict["pca"]:
		pca_components = np.load(_model+'/pca.npy')

samples = preprocessing.tp_sample.get_samples(_essay_folder)
texts = [sample.text for sample in samples]
test_matrix, _, _ = preprocessing.preprocess(texts, words_src = _words)
if pca_components is not None:
	test_matrix = np.matmul(test_matrix, pca_components.T)
if _norm_dict is not None:
	test_matrix, _, _ = preprocessing.normalize(test_matrix, norm_info = _norm_dict)
if _type == "NN":
	model = models.Neural_Network.load(_model)
	result = model.predict(test_matrix)
	df = pandas.DataFrame(preprocessing.dist_softmax(result.T).T)
	df["name"] = [sample.get_identifier() for sample in samples]
	df.to_csv("dist.csv", index = False)
	result = preprocessing.dists_to_labels(result, _grouped_sections)

else:
	model = models.SVR.load(_model)
	result = model.predict(test_matrix)
	
_result_count = {s: 0 for s in _grouped_sections}
for i in range(result.shape[0]):
	section = _grouped_sections[int(result[i])]
	print("%s\t%s"%(samples[i].get_identifier(), section))
	_result_count[section] += 1

print(_result_count)