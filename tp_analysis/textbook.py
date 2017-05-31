import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import words

infile = 'Nature-2nd-Edited.pdf'
outfile = 'top30.txt'
topn = 30

'''
chapter_pg = [
['1a',15,19]
]
'''
chapter_pg = [
['1a',15,19],
['1b',21,25],
['2',27,57],
['3a',59,72],
['3b',73,79],
['4',83,105],
['5',107,151],
['6',153,168],
['7',171,188],
['8',189,204],
['9',205,228],
['10a',229,253],
['10b',263,267],
['11a',269,283],
['11b',285,300]
]

chap_texts = {}
is_init = False

# The stop words listed in
# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
# would be ignored.

def init():
	global is_init
	pdfReader = PyPDF2.PdfFileReader(open(infile,'rb'))
	pgn = pdfReader.numPages
	print('Reading textbook...')
	print('> Number of pages = %d' % pgn)
	for ch in chapter_pg:
		print("> Initializing chapter %s"%ch[0])
		chapter_text = []
		for i in range(ch[1]-1,ch[2]):
			pg = pdfReader.getPage(i).extractText()
			chapter_text.append(pg)
		chapter_text = ' '.join(chapter_text)
		chap_texts[ch[0]] = chapter_text
	is_init = True

def getOrderedText():
	if not is_init:
		init()

	texts = []
	for [ch, _, _] in chapter_pg:
		texts.append(chap_texts[ch])
	return texts

def getTfidfVectorizer():
	vectorizer = TfidfVectorizer(stop_words = 'english')
	vectorizer.fit(getOrderedText())
	return vectorizer

def getTopVocabs(ch, n = 30):
	if not is_init:
		init()
	if ch not in chap_texts:
		raise Exception('Invalid Chapter ch')

	vectorizer = CountVectorizer(stop_words = 'english')
	freq = vectorizer.fit_transform([chap_texts[ch]]).toarray()[0]
	word_index_table = vectorizer.vocabulary_
	word_freq_pair = []

	# Retrieve frequency of each word
	for vocab in word_index_table:
		index = word_index_table[vocab]
		pair = (vocab, freq[index])
		word_freq_pair.append(pair)

	word_freq_pair = sorted(word_freq_pair, key = lambda x: x[1], reverse = True)
	
	i, count = (0, 0)
	while count < n and i < len(word_freq_pair):
		if word_freq_pair[i][0].isalpha() and len(word_freq_pair[i][0]) >= 3:
			count += 1
			yield word_freq_pair[i]
		i += 1

if __name__ == '__main__':
	f = open(outfile,'w', encoding='utf-8')
	for ch in chapter_pg:
		i = 0
		print('\n{:=^26}\n'.format(' Chapter '+ch[0]+' '), file = f)
		for x in getTopVocabs(ch[0], topn):
			print('%4d: %-15s %4d' % (i+1, x[0], x[1]), file = f)
			i += 1
	f.close()