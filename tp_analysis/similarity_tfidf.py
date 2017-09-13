from sklearn.feature_extraction.text import TfidfVectorizer
import textbook
import pandas
import preprocessing

sample_folder = "./samples"
out_file = "similarity.csv"
n_key_vocabs = 50
ngram_rng = (1, 3)

chs = ['1a','1b','2','3a','3b','4','5','6','7','8','9','10a','10b','11a','11b']

samples = preprocessing.tp_sample.get_samples(sample_folder)
samples_textbook = [sample.text for sample in samples]+textbook.getOrderedText(chs = chs)
vocabularies = {}
for ch in chs:
	ch_vocabs = textbook.getTopVocabs(ch, n = n_key_vocabs, ngram_rng = ngram_rng)
	for vocab, freq in ch_vocabs:
		vocabularies[vocab] = 1
vectorizer = TfidfVectorizer(ngram_range = ngram_rng,  stop_words = 'english', vocabulary = vocabularies.keys())
vectorizer.fit(textbook.getOrderedText(chs = chs))

tfidf = vectorizer.transform(samples_textbook)

similarity = (tfidf*tfidf.T).A
similarity = similarity[0:len(samples), len(samples):]

similarity_df = pandas.DataFrame(similarity, columns = textbook.getChapterTitles())
similarity_df.index = [sample.get_identifier() for sample in samples]

similarity_df.to_csv(out_file)
