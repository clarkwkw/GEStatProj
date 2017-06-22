from sklearn.feature_extraction.text import CountVectorizer
import sample

_words = []
_sample_folder = "./samples"

def preprocess(words, samples):
	vocabs = {}
	for i in range(len(words)):
		vocabs[words[i]] = i
	vectorizer = CountVectorizer(vocabulary = vocabs)

	texts = [sample.text for sample in samples]
	result = vectorizer.transform(texts)
	return result

if __name__ == '__main__':
	samples = sample.get_samples(_sample_folder)
	samples_X = preprocess(_words, samples)
	samples_Y = [sample.understand for sample in samples]