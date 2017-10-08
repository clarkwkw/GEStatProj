import preprocessing
import random
from sklearn.cluster import KMeans
import numpy as np

_news_dir = "./news_crawler/guardian/texts"
_model = "SVM"
_min_word_count = 400
_train_ratio = 0.8
_max_thread = 4
_reduction = "ipca"
_reduce_n_attr = 1000
_max_sample_count = 10000
_stem_words = True

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
train_matrix, test_matrix, words = preprocessing.preprocess(train_texts, test_texts, words_src = "samples", normalize_flag = False, reduction = _reduction, reduce_n_attr = _reduce_n_attr, stem_words = _stem_words)

print("Generating labels..")
train_labels = preprocessing.samples_to_label(train_samples, _section_filter, get_section)
test_labels = preprocessing.samples_to_label(test_samples, _section_filter, get_section)

print("Training..")
kmeans = KMeans(n_clusters = len(_section_filter))
reference_output = kmeans.fit_predict(train_matrix)

# count[c, j]: for the cth cluster, how many texts belong to the jth section
count = np.zeros((len(_section_filter), len(_section_filter)))
for i in range(reference_output.shape[0]):
	c = reference_output[i]
	j = _section_filter.index(get_section(train_samples[i]))
	count[c, j] += 1 

cluster_section_map = count.argmax(axis = 1)

test_predict = kmeans.predict(test_matrix)
for i in range(test_predict.shape[0]):
	test_predict[i] = cluster_section_map[test_predict[i]]

accuracy = np.mean(test_predict == test_labels)

print("accuracy %.3f"%accuracy)