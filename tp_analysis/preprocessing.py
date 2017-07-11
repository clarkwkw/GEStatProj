from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA
import sample
import textbook

pca_strategies = ["pca_idf", "pca_textbook_idf", "pca_textbook_tfidf"]

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

def preprocess_by(train_samples, valid_samples = [], strategy = "", **kwargs):
	global pca_components
	if strategy == "idf":
		return by_idf(train_samples, valid_samples, **kwargs)
	elif strategy == "predefined_words":
		return by_predefined_words(train_samples, valid_samples, **kwargs)
	elif strategy == "textbook_idf":
		return by_textbook_idf(train_samples, valid_samples, **kwargs)
	elif strategy == "textbook_tfidf":
		return by_textbook_tfidf(train_samples, valid_samples, **kwargs)
	elif strategy == "pca_textbook_idf":
		return with_pca(train_samples, valid_samples, by_textbook_idf, **kwargs)
	elif strategy == "pca_idf":
		return with_pca(train_samples, valid_samples, by_idf, **kwargs)
	elif strategy == "pca_textbook_tfidf":
		return with_pca(train_samples, valid_samples, by_textbook_tfidf, **kwargs)
	else:
		raise Expcetion("Unexpected strategy.")

# preprocess_func: by_idf/ by_textbook_idf/ by_textbook_tfidf
def with_pca(train_samples, valid_samples = [], preprocess_func = None, n_attribute = 50, **kwargs):
	train_matrix, valid_matrix, words, _ = preprocess_func(train_samples, valid_samples, use_all = True, **kwargs)
	pca = PCA(n_components = n_attribute)
	train_matrix = pca.fit_transform(train_matrix)
	valid_matrix = pca.transform(valid_matrix)
	return train_matrix, valid_matrix, words, pca.components_

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
	return (train_matrix, valid_matrix, words, None)

def by_idf(train_samples, valid_samples = [], top = 0, bottom = 0, use_all = False):
	vectorizer = TfidfVectorizer(stop_words = 'english')
	train_texts = [sample.text for sample in train_samples]
	vectorizer.fit(train_texts)
	idf_tuples = []
	for vocab in vectorizer.vocabulary_:
		index = vectorizer.vocabulary_[vocab]
		idf = vectorizer.idf_[index]
		idf_tuples.append((vocab, idf, index))

	idf_tuples = sorted(idf_tuples, key = lambda x: x[1], reverse = True)
	selected_tuples = []
	if use_all or top+bottom >= len(idf_tuples):
		selected_tuples = idf_tuples
	else:
		selected_tuples = idf_tuples[0:top]+idf_tuples[(len(idf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)

def by_textbook_idf(train_samples, valid_samples = [], top = 0, bottom = 0, use_all = False):
	vectorizer = textbook.getTfidfVectorizer()
	idf_tuples = []
	for vocab in vectorizer.vocabulary_:
		index = vectorizer.vocabulary_[vocab]
		idf = vectorizer.idf_[index]
		idf_tuples.append((vocab, idf, index))

	idf_tuples = sorted(idf_tuples, key = lambda x: x[1], reverse = True)
	selected_tuples = []
	if use_all or top+bottom >= len(idf_tuples):
		selected_tuples = idf_tuples
	else:
		selected_tuples = idf_tuples[0:top]+idf_tuples[(len(idf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)

def by_textbook_tfidf(train_samples, valid_samples = [], top = 0, bottom = 0, use_all = False):
	vectorizer = textbook.getTfidfVectorizer()
	text = '\n'.join(textbook.getOrderedText())
	textbook_tfidf = vectorizer.transform([text]).toarray()[0]
	tfidf_tuples = []
	for vocab in vectorizer.vocabulary_:
		index = vectorizer.vocabulary_[vocab]
		tfidf = textbook_tfidf[index]
		tfidf_tuples.append((vocab, tfidf, index))
	tfidf_tuples = sorted(tfidf_tuples, key = lambda x: x[1], reverse = True)
	if use_all or top+bottom >= len(tfidf_tuples):
		selected_tuples = tfidf_tuples
	else:
		selected_tuples = tfidf_tuples[0:top]+tfidf_tuples[(len(tfidf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)