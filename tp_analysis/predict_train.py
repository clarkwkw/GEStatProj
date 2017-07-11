import json
import neural_network
import numpy as np
import os
import preprocessing
import random
import sample
import tensorflow as tf

_sample_folder = "./samples"
_model_folder = "./models"
_words = ["nature", "science", "motion", "equal", "angle", "text", "time", "dialogue", "dna", "species", "new", "did", "straight", "point", "line", "force", "chinese", "aristotle", "life", "natural", "way", "world", "let", "modern", "angles", "change", "body", "greater", "china", "like", "given", "mathematical", "work", "things", "form", "selection", "thought", "great", "ab", "does", "place", "different", "called", "lines", "earth", "long", "fact", "make", "revolution", "triangle"]
_attributes = 50
_strategy = "idf"
_strategy_parameters = {
	#"words": _words
	"top": 15,
	"bottom": 35
}

learning_rate = 0.001
training_epocs = 100000
display_step = 100
n_hidden_1 = 10
cross_valid = 5
pca_components = None

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

def mkdir(dir):
	try:
		os.mkdir(dir)
	except FileExistsError:
		pass

if len(os.listdir(_model_folder)) > 0:
	ans = input("Found something in '%s', which may be overwitten.\nProceed? [y/n]: "%_model_folder)
	if ans.lower() == 'n':
		exit(-1)

for k in range(4):
	samples = sample.get_samples(_sample_folder)
	random.shuffle(samples)
	batches = preprocessing.batch_data(samples, cross_valid)
	for i in range(cross_valid):
		valid_samples = batches[i]
		train_samples = []
		mkdir("%s/%d"%(_model_folder, i+1))
		for j in range(cross_valid):
			if j != i:
				train_samples.extend(batches[j])
		train_matrix, valid_matrix, words, pca_components = preprocessing.preprocess_by(train_samples, valid_samples, _strategy, **_strategy_parameters)
		train_labels = np.asarray([get_label(sample) for sample in train_samples])
		valid_labels = np.asarray([get_label(sample) for sample in valid_samples])
		nn = neural_network.Neural_Network()
		nn.configure_parameters(learning_rate, training_epocs, display_step)
		nn.configure_network(weights, biases, network)
		valid_mse = nn.train(train_matrix, train_labels, valid_matrix, valid_labels, "%s/%d/"%(_model_folder, i+1), False)
		conf = {
			"attributes": _attributes,
			"words": words,
			"valid_mse": valid_mse,
			"preprocess_strategy": _strategy
		}
		print("Fold %2d: %.4f"%(i+1, valid_mse))
		with open("%s/%d/conf.json"%(_model_folder, i+1), "w") as f:
			f.write(json.dumps(conf, indent = 4, sort_keys = True))
		if pca_components is not None:
			np.save("%s/%d/pca.npy"%(_model_folder, i+1), pca_components)
