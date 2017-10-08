import json
import models
import numpy as np
import os
import preprocessing
import random
import tensorflow as tf

_essay_folder = "./samples"
_model = "./output"
_type = "SVM"
_grouped_sections = ["education", "science & technology", "environment", "global-development"]
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
	preprocessing.dists_to_labels(result, _grouped_sections)

else:
	model = models.SVR.load(_model)
	result = model.predict(test_matrix)
	
_result_count = {}
for i in range(result.shape[0]):
	section = _grouped_sections[int(result[i])]
	if section not in _result_count:
		_result_count[section] = 1
	else:
		_result_count[section] += 1

print(_result_count)