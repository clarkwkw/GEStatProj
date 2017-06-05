import os
import numpy as np
from sample import Sample
import textbook
import nltk
import pandas

sample_folder = "./samples"
out_file = "similarity.csv"
n_key_vocabs = 30

try:
	files = os.listdir(sample_folder)
	sample_names = []
	for file in files:
		file_name = file.split('.')
		if file_name[len(file_name) - 1] == 'txt':
			sample_names.append(file)

except FileNotFoundError:
	print("Folder 'samples' does not exist, abort,")
	exit(-1)

def normalize(v):
	length = np.sum(v)
	return np.divide(v, length)

def dict_to_arr(dict, fields = []):
	result = []
	for field in fields:
		result.append(dict[field])
	result = np.reshape(result, len(result))
	return result

def cal_similarity(v1, v2):
	v1 = normalize(v1)
	v2 = normalize(v2)
	dot_product = np.dot(v1, v2)
	return dot_product

samples = [Sample(sample_folder+'/'+x) for x in sample_names]
similarity = np.zeros((len(samples), len(textbook.chapter_pg)))
key_vocabs_all = {}
key_vocabs_chapters = []
chapter_vects = []

# Get important vocabs of each chapter
for j in range(len(textbook.chapter_pg)):
	ch = textbook.chapter_pg[j][0]
	key_vocabs = []
	chapter_vect = []
	for (vocab, freq) in textbook.getTopVocabs(ch, n_key_vocabs):
		key_vocabs.append(vocab)
		chapter_vect.append(freq)
		key_vocabs_all[vocab] = 0
	chapter_vect = np.reshape(chapter_vect, len(chapter_vect))
	key_vocabs_chapters.append(key_vocabs)
	chapter_vects.append(chapter_vect)

# For each sample, count the appearance of important vocabs
# Then, calculate cosine similarity
for i in range(len(samples)):
	sample_vocab_freq = dict(key_vocabs_all)
	for token in nltk.word_tokenize(samples[i].text):
		if token in sample_vocab_freq:
			sample_vocab_freq[token] += 1
	for j in range(len(textbook.chapter_pg)):
		sample_vect = dict_to_arr(sample_vocab_freq, key_vocabs_chapters[j])
		similarity[i, j] = cal_similarity(sample_vect, chapter_vects[j])

chapter_titles = [ch[0] for ch in textbook.chapter_pg]
similarity_df = pandas.DataFrame(similarity, columns = chapter_titles)
similarity_df.index = [sample.name for sample in samples]

similarity_df.to_csv(out_file)