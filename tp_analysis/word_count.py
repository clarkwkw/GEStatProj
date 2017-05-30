import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import words

infile = 'Nature-2nd-Edited.pdf'
outfile = 'top30.txt'
topn = 30

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

chap_vectorizers = {}
chap_stats = {}
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
		print("> Initiating chapter %s"%ch[0])
		vectorizer = CountVectorizer(stop_words = 'english')
		chapter_text = []
		for i in range(ch[1]-1,ch[2]):
			pg = pdfReader.getPage(i).extractText()
			chapter_text.append(pg)
		chapter_text = ' '.join(chapter_text)
		chap_stats[ch[0]] = vectorizer.fit_transform([chapter_text]).toarray()[0]
		chap_vectorizers[ch[0]] = vectorizer

	is_init = True

def getTopVocabs(ch, n = 30):
	if not is_init:
		init()
	if ch not in chap_vectorizers:
		raise Exception('Invalid Chapter ch')
	freq = dict(chap_vectorizers[ch].vocabulary_)
	
	# Retrieve frequency of each word
	for vocab in freq:
		freq[vocab] = chap_stats[ch][freq[vocab]]
	tuples = [x for x in list(freq.items())]
	tuples = sorted(tuples, key = lambda x: x[1], reverse = True)
	
	i, count = (0, 0)
	while count < n and i < len(tuples):
		#if tuples[i][0] in words.words():
		if tuples[i][0].isalpha():
			count += 1
			yield tuples[i]
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