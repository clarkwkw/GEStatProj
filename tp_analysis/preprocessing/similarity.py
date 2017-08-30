import textbook

def tb_similarity(samples, chs = None):
	samples_textbook = [sample.text for sample in samples]+textbook.getOrderedText(chs = chs)
	vectorizer = textbook.getTfidfVectorizer(chs = chs)
	tfidf = vectorizer.transform(samples_textbook)
	similarity = (tfidf*tfidf.T).A
	similarity = similarity[0:len(samples), len(samples):]
	return similarity