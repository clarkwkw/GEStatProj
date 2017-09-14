import preprocessing
import random
from models import SVM, Neural_Network
import numpy as np

_sample_folder = "./samples"
_batch_name = "TP1"
_train_ratio = 0.75
_classes = ["Q1", "Q2", "Q3", "Q4"]

# SVM / NN
_model = "SVM"

# NN parameters
_learning_rate = 1
_hidden_nodes = []

def get_question(sample):
	return sample.question

samples = preprocessing.tp_sample.get_samples(_sample_folder)
samples = [s for s in samples if s.batch_name == _batch_name and s.question is not None]
random.shuffle(samples)
n_samples = len(samples)
train_samples = samples[0:int(n_samples*_train_ratio)]
test_samples = samples[int(n_samples*_train_ratio):n_samples]

print("Samples distribution:", preprocessing.samples_statistics(samples, _classes, get_question))
print("Train set distribution:", preprocessing.samples_statistics(train_samples, _classes, get_question))
print("Test set distribution:", preprocessing.samples_statistics(test_samples, _classes, get_question))

train_texts = [sample.text for sample in train_samples]
test_texts = [sample.text for sample in test_samples]
train_matrix, test_matrix, words = preprocessing.preprocess(train_texts, test_texts, words_src = "samples", normalize_flag = False)

if _model == "SVM":
	train_labels = preprocessing.samples_to_label(train_samples, _classes, get_question)
	test_labels = preprocessing.samples_to_label(test_samples, _classes, get_question)

	model = SVM()
	model.train(train_matrix, train_labels)
	predict = model.predict(test_matrix)

elif _model == "NN":
	train_dists = preprocessing.samples_to_dists(train_samples, _classes, get_question)
	test_dists = preprocessing.samples_to_dists(test_samples, _classes, get_question)
	model = Neural_Network(_n_factors = train_matrix.shape[1], _learning_rate = _learning_rate, _hidden_nodes = _hidden_nodes, _last_layer = len(_classes))
	model.train(train_matrix, train_dists, test_matrix, test_dists)
	predict = model.predict(test_matrix)
	predict = preprocessing.dists_to_labels(predict, _classes)
	test_labels = preprocessing.samples_to_label(test_samples, _classes)

else:
	raise Exception("Unknown model flag '%s'"%str(_model))

accuracy = np.mean(predict == test_labels)

print("accuracy %.3f"%accuracy)