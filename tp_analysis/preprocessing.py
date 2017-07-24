import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA, TruncatedSVD
import sample
import textbook

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

def by_predefined_words(train_samples, valid_samples = [], words = None):
	vocabs = {}
	if words is None:
		words = textbook.getTopVocabs("all", 30)

	for i in range(len(words)):
		vocabs[words[i]] = i
	vectorizer = CountVectorizer(vocabulary = vocabs)

	train_texts = [sample.text for sample in train_samples]
	valid_texts = [sample.text for sample in valid_samples]
	train_matrix = vectorizer.transform(train_texts).todense()
	valid_matrix = vectorizer.transform(valid_texts).todense()
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

def preprocess(train_samples, valid_samples = [], normalize_flag = True, top = 0, bottom = 0, use_all = False,  selection = "tf", words = [], pca_n_attr = None, lsa_n_attr = None, savedir = None):
	vectorizer = None
	if type(words) is list:
		train_matrix, valid_matrix, words = by_predefined_words(train_samples, valid_samples, words)
	else:
		if words == "textbook":
			vect_texts =  ['\n'.join(textbook.getOrderedText())]
			vectorizer = textbook.getTfidfVectorizer()
			vectorizer.fit(vect_texts)
		elif words == "samples":
			vect_texts = [sample.text for sample in train_samples]
			vectorizer = TfidfVectorizer(stop_words = 'english')
			vectorizer.fit(vect_texts)
		else:
			raise Exception("Unexpected type for 'words'")

		if selection == "tfidf":
			tfidf_matrix = vectorizer.transform(vect_texts).toarray()[0]
		tuples = []
		for vocab in vectorizer.vocabulary_:
			index = vectorizer.vocabulary_[vocab]
			if selection == "idf":
				score = vectorizer.idf_[index]
			elif selection == "tfidf":
				score = tfidf_matrix[index]
			else:
				raise Exception("Unexpected selection type")
			tuples.append((vocab, score, index))
		tuples = sorted(tuples, key = lambda x: x[1], reverse = True)
		selected_tuples = []
		if use_all or top + bottom >= len(tuples):
			selected_tuples = tuples
		else:
			selected_tuples = tuples[0:top] + tuples[(len(tuples)-bottom):]
		selected_words = [tup[0] for tup in selected_tuples]
		train_matrix, valid_matrix, words = by_predefined_words(train_samples, valid_samples, selected_words)

	if type(pca_n_attr) is int and type(lsa_n_attr) is int:
		raise Exception("Cannot perform PCA and LSA at the same time")
	
	pca_components, norm_info = None, None
	if type(pca_n_attr) is int:
		pca = PCA(n_components = pca_n_attr)
		train_matrix = pca.fit_transform(train_matrix)
		valid_matrix = pca.transform(valid_matrix)
		pca_components = pca.components_

	elif type(lsa_n_attr) is int:
		lsa = TruncatedSVD(n_components = lsa_n_attr)
		train_matrix = lsa.fit_transform(train_matrix)
		valid_matrix = lsa.transform(valid_matrix)
		pca_components = lsa.components_

	if normalize_flag:
		train_matrix, valid_matrix, norm_info = normalize(train_matrix, valid_matrix)
	if savedir is not None:
		preprocess = {
			"words": words, 
			"pca": type(pca_n_attr) is int or type(lsa_n_attr) is int,
		}
		if normalize_flag:
			preprocess["norm_info"] = norm_info
		with open(savedir+'/preprocess.json', "w") as f:
			f.write(json.dumps(preprocess, indent = 4))
		if savedir is not None:
			np.save(savedir+"/pca.npy", pca_components)

	return train_matrix, valid_matrix, words