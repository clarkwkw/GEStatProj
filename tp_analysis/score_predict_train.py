import json
from models import Neural_Network, SVR
import numpy as np
import os
import preprocessing
import random

_sample_folder = "./samples"
_model_folder = "./output"
_words = ["nature", "science", "motion", "equal", "angle", "text", "time", "dialogue", "dna", "species", "new", "did", "straight", "point", "line", "force", "chinese", "aristotle", "life", "natural", "way", "world", "let", "modern", "angles", "change", "body", "greater", "china", "like", "given", "mathematical", "work", "things", "form", "selection", "thought", "great", "ab", "does", "place", "different", "called", "lines", "earth", "long", "fact", "make", "revolution", "triangle"]
_model_type = "NN"
_name_filter = "KK201617T1"

# Preprocessing Parameters
_attributes = 50
_normalize = False
_filter_samples = False
_high_portion = 0.15
_low_portion = 0.15
_strategy_parameters = {
	"ngram_rng": (1, 1),
	"selection": "idf",
	"words": "textbook",
	"use_all": True,
	"pca_n_attr": 50
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
		samples = preprocessing.tp_sample.get_samples(_sample_folder)
		if _name_filter is not None:
			samples = [s for s in samples if s.name == _name_filter]
		#print(np.var([get_label(s) for s in samples]))
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
				train_samples = preprocessing.score_portion(train_samples, get_label, _high_portion, _low_portion)
			train_matrix, valid_matrix, words = preprocessing.preprocess(train_samples, valid_samples, normalize_flag = _normalize, savedir = savedir, **_strategy_parameters)
			train_labels = np.asarray([get_label(sample) for sample in train_samples])
			valid_labels = np.asarray([get_label(sample) for sample in valid_samples])
			model, valid_mse = None, None
			if _model_type == "NN":
				model = Neural_Network(_attributes, _hidden_nodes = hidden_nodes, _learning_rate = learning_rate)
				valid_mse = model.train(train_matrix, train_labels, valid_matrix, valid_labels, max_iter = 15000)
			else:
				model = SVR(**_svm_parameters)
				valid_mse = model.train(train_matrix, train_labels, valid_matrix, valid_labels)
			model.save(savedir)
			model.destroy()

			print("Fold %2d: %.4f"%(i+1, valid_mse))

if __name__ == "__main__":
	main(1, False)
	'''
	while _strategy_parameters["bottom"] >= 0:
		print("%s-%s: %d, %d"%(_strategy_parameters["words"], _strategy_parameters["selection"], _strategy_parameters["top"], _strategy_parameters["bottom"]))
		main(4, True)
		_strategy_parameters["top"] += 5
		_strategy_parameters["bottom"] -= 5
	'''