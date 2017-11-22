import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA, TruncatedSVD, IncrementalPCA, SparsePCA
import textbook
import nltk.stem

stemmer = nltk.stem.SnowballStemmer('english')
class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
		return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

class StemmedCountVectorizer(CountVectorizer):
	def build_analyzer(self):
		analyzer = super(StemmedCountVectorizer, self).build_analyzer()
		return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

def batch_data(series, batch_count):
	length = len(series)
	batch_size = length // batch_count
	arr = []
	start = 0
	for i in range(batch_count):
		end = start + batch_size + (i < length % batch_count)
		if end > length:
			end = length
		arr.append(series[start:end])
		start = end
	return arr

def by_predefined_words(train_texts, valid_texts = [], words = None, force_dense = True):
	vocabs = {}
	if words is None:
		words = textbook.getTopVocabs("all", 30)

	for i in range(len(words)):
		vocabs[words[i]] = i
	vectorizer = CountVectorizer(vocabulary = vocabs)

	train_matrix = vectorizer.transform(train_texts)
	valid_matrix = vectorizer.transform(valid_texts)

	if force_dense:
		train_matrix, valid_matrix = train_matrix.todense(), valid_matrix.todense()

	return (train_matrix, valid_matrix, words)

def normalize(train_matrix, valid_matrix = None, norm_info = None):
	n_cols = None
	norm_dict = {'total': train_matrix.shape[1]}
	if norm_info is not None:
		n_cols = norm_info["total"]
	else:
		n_cols = train_matrix.shape[1]

	for i in range(n_cols):
		mean, std = None, None
		if norm_info is not None:
			mean = norm_info["%d"%i]["mean"]
			std = norm_info["%d"%i]["std"]
		else:
			mean = np.mean(train_matrix[:, i])
			std = np.std(train_matrix[:, i])
			norm_dict[i] = {"mean": mean, "std": std}

		if std != 0:
			train_matrix[:, i] = (train_matrix[:, i] - mean)/std
			if valid_matrix is not None:
				valid_matrix[:, i] = (valid_matrix[:, i] - mean)/std
		else:
			train_matrix[:, i] = 0.5
			if valid_matrix is not None:
				valid_matrix[:, i] = 0.5
		
	return train_matrix, valid_matrix, norm_dict

# Perform 3 steps to generate training/ validating texts:
# 1. Construct the bag of words
#		Parameters:
#			ngram_rng: tuple, the lower and uppper bound of the length of a ngram
#			words_src: "textbook"/"samples" / list of strings, the source to consider
#			tb_chs: list of textbook chapters/ None, when words_src = "textbook", the chapters of textbook to consider
#			selection: None/ "tfidf"/ "idf", strategy to select the bag of words
#			select_top, select_bottom: integer, no. of words to select according the top/ bottom values of selection strategy
#	
# 2. Dimensionality reduction
#		Parameters:
#			reduction: None/ "pca"/ "lsa"/ "ipca", strategy for dimensionality reduction
#			reduce_n_attr: integer, desired no. of dimensions after reduction	
#
# 3. Normalization
#		Parameters:
#			normalize_flag: boolean, if set to true, columns will be normalized to 0 mean and variance 1
#
# Other parameters:
#	save_dir: string/ None, save preprocessing settings to the specified directory if not None
def preprocess(train_texts, valid_texts = [], normalize_flag = False, ngram_rng = (1,1), words_src = None, tb_chs = None, selection = None, select_top = 0, select_bottom = 0, reduction = None, reduce_n_attr = None, stem_words = False, savedir = None):
	vectorizer, vect_texts = None, None
	if type(words_src) is list:
		train_matrix, valid_matrix, words = by_predefined_words(train_texts, valid_texts, words_src)
	else:
		if words_src == "textbook":
			vect_texts = textbook.getOrderedText(chs = tb_chs)
			if stem_words:
				vectorizer = textbook.getTfidfVectorizer(ngram_rng, chs = tb_chs)
			else:
				vectorizer = StemmedTfidfVectorizer(ngram_range = ngram_rng, stop_words = 'english')
				vectorizer.fit(textbook.getOrderedText(tb_chs))
		elif words_src == "samples":
			vect_texts = train_texts
			if stem_words:
				vectorizer = StemmedTfidfVectorizer(ngram_range = ngram_rng, stop_words = 'english')
			else:
				vectorizer = TfidfVectorizer(ngram_range = ngram_rng, stop_words = 'english')
			vectorizer.fit(train_texts)
		elif isinstance(words_src, TfidfVectorizer):
			vectorizer = words_src
		else:
			raise Exception("Unexpected value for 'words_src'")

		if selection == "tfidf":
			tfidf_matrix = vectorizer.transform(vect_texts).toarray()[0]
		tuples = []
		for vocab in vectorizer.vocabulary_:
			index = vectorizer.vocabulary_[vocab]
			if selection == "idf":
				score = vectorizer.idf_[index]
			elif selection == "tfidf":
				score = tfidf_matrix[index]
			elif selection is None:
				score = vectorizer.idf_[index]
			else:
				raise Exception("Unexpected selection type")
			tuples.append((vocab, score, index))
			
		
		selected_tuples = []
		if selection is None or select_top + select_bottom >= len(tuples):
			selected_tuples = tuples
		elif select_top + select_bottom > 0:
			tuples = sorted(tuples, key = lambda x: x[1], reverse = True)
			selected_tuples = tuples[0:select_top] + tuples[(len(tuples)-select_bottom):]
		else:
			raise Exception("Must specify 'select_top'/'select_bottom' when 'selection' is not None")

		selected_words = [tup[0] for tup in selected_tuples]
		train_matrix, valid_matrix, words = by_predefined_words(train_texts, valid_texts, selected_words, force_dense = reduction not in ["lsa"])
		
	pca_components, norm_info = None, None
	reductor = None
	if reduction is not None:
		if reduction == "pca":
			reductor = PCA(n_components = reduce_n_attr)
		elif reduction == "lsa":
			reductor = TruncatedSVD(n_components = reduce_n_attr)
		elif reduction == "ipca":
			reductor = IncrementalPCA(n_components = reduce_n_attr)
		else:
			raise Exception("Unexpected reduction strategy '%s'"%reduction)

		train_matrix = reductor.fit_transform(train_matrix)
		valid_matrix = reductor.transform(valid_matrix)
		pca_components = reductor.components_

	if normalize_flag:
		train_matrix, valid_matrix, norm_info = normalize(train_matrix, valid_matrix)

	if savedir is not None:
		preprocess = {
			"words": words, 
			"pca": reduction is not None
		}
		if normalize_flag:
			preprocess["norm_info"] = norm_info
		with open(savedir+'/preprocess.json', "w") as f:
			f.write(json.dumps(preprocess, indent = 4))
		if reduction is not None:
			np.save(savedir+"/pca.npy", pca_components)

	return train_matrix, valid_matrix, words
