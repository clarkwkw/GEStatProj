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

chapter_titles = [ch[0] for ch in textbook.chapter_pg]
samples = [Sample(sample_folder+'/'+x) for x in sample_names]
samples_textbook = [sample.text for sample in samples]+textbook.getOrderedText()
vectorizer = textbook.getTfidfVectorizer()
tfidf = vectorizer.transform(samples_textbook)
similarity = (tfidf*tfidf.T).A
similarity = similarity[0:len(samples), len(samples):]

similarity_df = pandas.DataFrame(similarity, columns = chapter_titles)
similarity_df.index = [sample.name for sample in samples]

similarity_df.to_csv(out_file)
