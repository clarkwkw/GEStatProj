import json
import neural_network
import numpy as np
import os
import preprocessing
import random
import sample
import tensorflow as tf

_sample_folder = "./samples"
_model = "./models/1"
_words = []
_init_para = None
pca_components = None


with open(_model+"/conf.json", "r") as f:
	conf = json.load(f)
	_words = conf["words"]
	_init_para = conf["init_para"]
	if conf["pca"]:
		pca_components = np.load(_model+'pca.npy')

def get_label(sample):
	return sample.understand

samples = sample.get_samples(_sample_folder)
test_matrix, _, _, _ = preprocessing.preprocess(samples, words = _words)
if pca_components is not None:
	test_matrix = np.matmul(test_matrix, pca_components.T)
nn = neural_network.Neural_Network(from_save = _model, **_init_para)
result = nn.test(test_matrix)
print([sample.understand for sample in samples])
print(result)