import json
import models
import numpy as np
import os
import preprocessing
import random
import tensorflow as tf
import pandas

_essay_folder = "./samples"
_model = "./output"
_grouped_sections = ['education', 'science & technology', 'environment', 'global-development', 'business', 'culture', 'politics']
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

result = pandas.DataFrame({"Name": [sample.get_identifier() for sample in samples]}, columns = ["Name"]+_grouped_sections)
for section in _grouped_sections:
	model = models.SVR.load("%s/%s"%(_model, section))
	result[section] = model.predict(test_matrix)

result.to_csv("essay_clustered.csv", index = False)