import filter
import json
import neural_network
import svm
import numpy as np
import os
import preprocessing
import random
import sample
import tensorflow as tf

_sample_folder = "./samples"
_model_folder = "./models"
_words = ["nature", "science", "motion", "equal", "angle", "text", "time", "dialogue", "dna", "species", "new", "did", "straight", "point", "line", "force", "chinese", "aristotle", "life", "natural", "way", "world", "let", "modern", "angles", "change", "body", "greater", "china", "like", "given", "mathematical", "work", "things", "form", "selection", "thought", "great", "ab", "does", "place", "different", "called", "lines", "earth", "long", "fact", "make", "revolution", "triangle"]
_model_type = "SVM"

# Preprocessing Parameters
_attributes = 50
_normalize = False
_filter_samples = False
_high_portion = 0.15
_low_portion = 0.15
_strategy_parameters = {
	"ngram_rng": (2, 3),
	"selection": "tfidf",
	"words": "samples",
	"use_all": True,
	"ipca_n_attr": 50
}
_svm_parameters = {
}

# Neural Network Parameters
learning_rate = 0.001
training_epocs = 100000
valid_step = 100
hidden_nodes = [10]
cross_valid = 5

def get_label(sample):
	return sample.think + sample.understand + sample.lang + sample.pres

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

			savedir = "%s/%d/"%(_model_folder, i+1)
			mkdir(savedir)
			
			for j in range(cross_valid):
				if j != i:
					train_samples.extend(batches[j])
			
			if _filter_samples:
				train_samples = filter.score_portion(train_samples, get_label, _high_portion, _low_portion)
			train_matrix, valid_matrix, words = preprocessing.preprocess(train_samples, valid_samples, normalize_flag = _normalize, savedir = savedir, **_strategy_parameters)
			train_labels = np.asarray([get_label(sample) for sample in train_samples])
			valid_labels = np.asarray([get_label(sample) for sample in valid_samples])
			model, valid_mse = None, None
			if _model_type == "NN":
				model = neural_network.Neural_Network(_attributes, hidden_nodes, learning_rate)
				valid_mse = model.train(train_matrix, train_labels, valid_matrix, valid_labels, max_iter = 15000)
			else:
				model = svm.SVR(**_svm_parameters)
				valid_mse = model.train(train_matrix, train_labels, valid_matrix, valid_labels)
			model.save(savedir)
			model.destroy()

			print("Fold %2d: %.4f"%(i+1, valid_mse))

if __name__ == "__main__":
	main(4, True)
	'''
	while _strategy_parameters["bottom"] >= 0:
		print("%s-%s: %d, %d"%(_strategy_parameters["words"], _strategy_parameters["selection"], _strategy_parameters["top"], _strategy_parameters["bottom"]))
		main(4, True)
		_strategy_parameters["top"] += 5
		_strategy_parameters["bottom"] -= 5
	'''