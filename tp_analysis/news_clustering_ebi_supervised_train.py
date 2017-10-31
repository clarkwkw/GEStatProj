import preprocessing
import random
from models import SVR
import numpy as np

_essays_dir = "./samples"
_n_key_vocabs = 1000
_ngram_rng = (1, 1)

_save_dir = "./output"

_news_dir = "./news_crawler/guardian/old/texts"
_min_word_count = 400
_train_ratio = 0.8
_max_thread = 4
_reduction = None
_reduce_n_attr = 1000
_max_sample_count = None
_stem_words = True

# Neural Network Parameters
_learning_rate = 0.001
_max_iter = 100000
_valid_step = 100
_hidden_nodes = [20]

_section_filter = ["business", "education", "science", "technology", "higher-education-network", "environment", "global-development", "culture", "politics"]
_section_group_map = {
	"education": "education",
	"science": "science & technology",
	"technology": "science & technology",
	"higher-education-network": "education",
	"environment": "environment",
	"global-development": "global-development",
	"business": "business",
	"culture": "culture",
	"politics": "politics"
}


def get_section(sample):
	return sample.section

def get_tfidfVectorizer_of_essay_top_tf_words():
	essays = preprocessing.tp_sample.get_samples(_essays_dir)
	count_vectorizer = preprocessing.StemmedCountVectorizer(ngram_range = _ngram_rng, stop_words = 'english')
	combined_essay = b'\n'.join([essay.text for essay in essays])
	freq = count_vectorizer.fit_transform([combined_essay]).toarray()[0]
	word_index_table = count_vectorizer.vocabulary_
	word_freq_pair = []

	# Retrieve frequency of each word
	for vocab in word_index_table:
		index = word_index_table[vocab]
		pair = (vocab, freq[index])
		word_freq_pair.append(pair)

	word_freq_pair = sorted(word_freq_pair, key = lambda x: x[1], reverse = True)
	i, count = (0, 0)

	chosen_words = []
	while count < _n_key_vocabs and i < len(word_freq_pair):
		if word_freq_pair[i][0].replace(" ", "").isalpha():
			count += 1
			chosen_words.append(word_freq_pair[i][0])
		i += 1

	vectorizer = preprocessing.StemmedTfidfVectorizer(ngram_range = _ngram_rng, stop_words = 'english', vocabulary = chosen_words)
	vectorizer.fit([essay.text for essay in essays])
	return vectorizer

print("Reading samples.. ")
news_samples = preprocessing.news_sample.get_samples_multithread(_news_dir, _max_thread, _max_sample_count)

print("Preprocessing.. ")
news_samples = [sample for sample in news_samples if sample.word_count >= _min_word_count and sample.section in _section_filter]

random.shuffle(news_samples)
n_samples = len(news_samples)
_sections = _section_filter
if _section_group_map is not None:
	_sections = {section: True for section in _section_group_map.values()}
	_sections = list(_sections.keys())
	print("Grouped sections:", _sections)
	for sample in news_samples:
		sample.section = _section_group_map[sample.section]
	
train_samples = news_samples[0:int(n_samples*_train_ratio)]
test_samples = news_samples[int(n_samples*_train_ratio):n_samples]

print("Samples distribution:", preprocessing.samples_statistics(news_samples, _sections, get_section))
print("Train set distribution:", preprocessing.samples_statistics(train_samples, _sections, get_section))
print("Test set distribution:", preprocessing.samples_statistics(test_samples, _sections, get_section))

train_texts = [sample.text for sample in train_samples]
test_texts = [sample.text for sample in test_samples]

tfidf_vectorizer = get_tfidfVectorizer_of_essay_top_tf_words()
print("Vectorizer built..")
train_matrix, test_matrix, words = preprocessing.preprocess(train_texts, test_texts, savedir = _save_dir, words_src = tfidf_vectorizer, normalize_flag = False, reduction = _reduction, reduce_n_attr = _reduce_n_attr,  stem_words = _stem_words)


for section in _sections:
	train_labels = preprocessing.samples_to_binary(train_samples, [section], get_section)
	test_labels = preprocessing.samples_to_binary(test_samples, [section], get_section)

	model = SVR()
	print("Training for %s section.. "%section)

	model.train(train_matrix, train_labels)
	predict = model.predict(test_matrix)
	accuracy = 0
	for i in range(predict.shape[0]):
		if predict[i] >= 0.5:
			predict[i] = 1
		else:
			predict[i] = 0
		if predict[i] == test_labels[i]:
			accuracy += 1.0
	accuracy /= predict.shape[0]
	model.save("%s/%s/"%(_save_dir,section))
	print("Accuracy: %.3f"%accuracy)

