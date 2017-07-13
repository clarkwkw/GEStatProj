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
_strategy_parameters = {
	#"selection": "tfidf",
	"words": _words,
	#"top": 45,
	#"bottom": 5
}

learning_rate = 0.001
training_epocs = 100000
valid_step = 100
hidden_nodes = [10]
cross_valid = 5
pca_components = None

def get_label(sample):
	return sample.understand

def mkdir(dir):
	try:
		os.mkdir(dir)
	except FileExistsError:
		pass


def main(run = 1, force_run = False):
	if not force_run and len(os.listdir(_model_folder)) > 0:
		ans = input("Found something in '%s', which may be overwitten.\nProceed? [y/n]: "%_model_folder)
		if ans.lower() == 'n':
			exit(-1)

	for k in range(run):
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
			train_matrix, valid_matrix, words, pca_components = preprocessing.preprocess(train_samples, valid_samples, **_strategy_parameters)
			train_labels = np.asarray([get_label(sample) for sample in train_samples])
			valid_labels = np.asarray([get_label(sample) for sample in valid_samples])
			nn = neural_network.Neural_Network(_attributes, hidden_nodes, learning_rate)
			valid_mse = nn.train(train_matrix, train_labels, valid_matrix, valid_labels, max_iter = 15000)
			nn.save("%s/%d/"%(_model_folder, i+1))
			nn.destroy()

			print("Fold %2d: %.4f"%(i+1, valid_mse))
			conf = {
				"init_para":{
					"_n_factors": _attributes,
					"_hidden_nodes": hidden_nodes
				},
				"words": words, 
				"valid_mse": valid_mse, 
				"pca": pca_components is not None
			}
			if pca_components is not None:
				np.save("%s/%d/pca.npy"%(_model_folder, i+1), pca_components)
			with open("%s/%d/conf.json"%(_model_folder, i+1), "w") as f:
				f.write(json.dumps(conf, indent = 4, sort_keys = True))

if __name__ == "__main__":
	main(1, False)
	'''
	while _strategy_parameters["bottom"] >= 0:
		print("%s-%s, %d, %d"%(_strategy_parameters["words"], _strategy_parameters["selection"], _strategy_parameters["top"], _strategy_parameters["bottom"]))
		main(4, True)
		_strategy_parameters["top"] += 5
		_strategy_parameters["bottom"] -= 5
	'''