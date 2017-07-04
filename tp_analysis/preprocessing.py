from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import sample
import textbook

def batch_data(series, batch_size):
	length = len(series)
	batches = length//batch_size
	if length%batch_size != 0:
		batches += 1
	arr = []
	for i in range(batches):
		start = i*batch_size
		end = (i+1)*batch_size
		if end > length:
			end = length
		arr.append(series[start:end])
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

def by_idf(train_samples, valid_samples = [], top = 0, bottom = 0):
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
	if top+bottom >= len(idf_tuples):
		selected_tuples = idf_tuples
	else:
		selected_tuples = idf_tuples[0:top]+idf_tuples[(len(idf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)

def by_textbook_idf(train_samples, valid_samples = [], top = 0, bottom = 0):
	vectorizer = textbook.getTfidfVectorizer()
	idf_tuples = []
	for vocab in vectorizer.vocabulary_:
		index = vectorizer.vocabulary_[vocab]
		idf = vectorizer.idf_[index]
		idf_tuples.append((vocab, idf, index))

	idf_tuples = sorted(idf_tuples, key = lambda x: x[1], reverse = True)
	selected_tuples = []
	if top+bottom >= len(idf_tuples):
		selected_tuples = idf_tuples
	else:
		selected_tuples = idf_tuples[0:top]+idf_tuples[(len(idf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)

def by_textbook_tfidf(train_samples, valid_samples = [], top = 0, bottom = 0):
	vectorizer = textbook.getTfidfVectorizer()
	text = '\n'.join(textbook.getOrderedText())
	textbook_tfidf = vectorizer.transform([text]).toarray()[0]
	tfidf_tuples = []
	for vocab in vectorizer.vocabulary_:
		index = vectorizer.vocabulary_[vocab]
		tfidf = textbook_tfidf[index]
		tfidf_tuples.append((vocab, tfidf, index))
	tfidf_tuples = sorted(tfidf_tuples, key = lambda x: x[1], reverse = True)
	if top+bottom >= len(tfidf_tuples):
		selected_tuples = tfidf_tuples
	else:
		selected_tuples = tfidf_tuples[0:top]+tfidf_tuples[(len(tfidf_tuples)-bottom):]
	selected_words = [tup[0] for tup in selected_tuples]
	return by_predefined_words(train_samples, valid_samples, selected_words)