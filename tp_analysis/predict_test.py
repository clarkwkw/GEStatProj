import json
import neural_network
import numpy as np
import os
import preprocessing
import random
import sample
import tensorflow as tf

_sample_folder = "./samples"
_model = "./models/1/"
_words = []
_attributes = 0
pca_components = None

n_hidden_1 = 10

with open(_model+"conf.json", "r") as f:
	conf = json.load(f)
	_words = conf["words"]
	_attributes = conf["attributes"]
	_strategy = conf["preprocess_strategy"]
	if _strategy in preprocessing.pca_strategies:
		pca_components = np.load(_model+'pca.npy')

def network(x, weights, biases):
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	out_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])
	return out_layer

weights = {
    'h1': tf.Variable(tf.random_normal([_attributes, n_hidden_1]), name = "w_h1"),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 1]), name = "w_out")
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1]), name = "b_b1"),
    'out': tf.Variable(tf.random_normal([1]), name = "b_out")
}

def get_label(sample):
	return sample.understand

samples = sample.get_samples(_sample_folder)
test_matrix, _, _, _ = preprocessing.by_predefined_words(samples, words = conf["words"])
if pca_components is not None:
	test_matrix = np.matmul(test_matrix, pca_components.T)
nn = neural_network.Neural_Network()
nn.configure_network(weights, biases, network)
result = nn.test(test_matrix, _model)
print(result)