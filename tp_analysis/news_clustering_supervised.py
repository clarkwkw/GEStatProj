import preprocessing
import random
from models import SVM, Neural_Network
import numpy as np

_news_dir = "./news_crawler/guardian/texts"
_model = "NN"
_min_word_count = 400
_train_ratio = 0.8
_max_thread = 4
_reduction = "ipca"
_reduce_n_attr = 1000
_max_sample_count = 10000
_stem_words = True

# Neural Network Parameters
_learning_rate = 0.001
_max_iter = 100000
_valid_step = 100
_hidden_nodes = [40]

_section_filter = ["education", "science", "technology", "higher-education-network", "environment", "global-development"]

def get_section(sample):
	return sample.section

print("Reading samples.. ")
news_samples = preprocessing.news_sample.get_samples_multithread(_news_dir, _max_thread, _max_sample_count)

print("Preprocessing.. ")
news_samples = [sample for sample in news_samples if sample.word_count >= _min_word_count and sample.section in _section_filter]

random.shuffle(news_samples)
n_samples = len(news_samples)
train_samples = news_samples[0:int(n_samples*_train_ratio)]
test_samples = news_samples[int(n_samples*_train_ratio):n_samples]

print("Samples distribution:", preprocessing.samples_statistics(news_samples, _section_filter, get_section))
print("Train set distribution:", preprocessing.samples_statistics(train_samples, _section_filter, get_section))
print("Test set distribution:", preprocessing.samples_statistics(test_samples, _section_filter, get_section))

train_texts = [sample.text for sample in train_samples]
test_texts = [sample.text for sample in test_samples]
train_matrix, test_matrix, words = preprocessing.preprocess(train_texts, test_texts, words_src = "samples", normalize_flag = False, reduction = _reduction, reduce_n_attr = _reduce_n_attr,  stem_words = _stem_words)

print("Generating labels..")
if _model == "SVM":
	train_labels = preprocessing.samples_to_label(train_samples, _section_filter, get_section)
	test_labels = preprocessing.samples_to_label(test_samples, _section_filter, get_section)

	model = SVM()
	print("Training.. ")
	model.train(train_matrix, train_labels)
	predict = model.predict(test_matrix)

elif _model == "NN":
	train_dists = preprocessing.samples_to_dists(train_samples, _section_filter, get_section)
	test_dists = preprocessing.samples_to_dists(test_samples, _section_filter, get_section)
	model = Neural_Network(_n_factors = train_matrix.shape[1], _learning_rate = _learning_rate, _hidden_nodes = _hidden_nodes, _last_layer = len(_section_filter))
	print("Training.. ")
	model.train(train_matrix, train_dists, test_matrix, test_dists, max_iter = _max_iter)
	predict = model.predict(test_matrix)
	predict = preprocessing.dists_to_labels(predict, _section_filter)
	test_labels = preprocessing.samples_to_label(test_samples, _section_filter, get_section)

else:
	raise Exception("Unknown model flag '%s'"%str(_model))

accuracy = np.mean(predict == test_labels)

print("accuracy %.3f"%accuracy)