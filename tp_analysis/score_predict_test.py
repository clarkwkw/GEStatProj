import json
import models
import numpy as np
import os
import preprocessing
import random
import tensorflow as tf

_sample_folder = "./samples"
_model = "./output/1"
_type = "NN"
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

def get_label(sample):
	return sample.understand

samples = preprocessing.tp_sample.get_samples(_sample_folder)
test_matrix, _, _ = preprocessing.preprocess(samples, words = _words)
if pca_components is not None:
	test_matrix = np.matmul(test_matrix, pca_components.T)
if _norm_dict is not None:
	test_matrix, _, _ = preprocessing.normalize(test_matrix, norm_info = _norm_dict)
if _type == "NN":
	model = models.Neural_Network.load(_model)
else:
	model = models.SVR.load(_model)
result = model.predict(test_matrix)
print([sample.understand for sample in samples])
print(result)