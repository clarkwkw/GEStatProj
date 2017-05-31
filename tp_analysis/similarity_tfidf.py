import os
import numpy as np
from sample import Sample
import textbook
import nltk

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

samples = [Sample(sample_folder+'/'+x) for x in sample_names]
samples_textbook = [sample.text for sample in samples]+textbook.getOrderedText()
vectorizer = textbook.getTfidfVectorizer()
tfidf = vectorizer.transform(samples_textbook)
similarity = (tfidf*tfidf.T).A
similarity = similarity[0:len(samples), len(samples):]

# Output to file
f = open(out_file, 'w')
for i in range(similarity.shape[1]):
	f.write(","+textbook.chapter_pg[i][0])
f.write("\n")
for i in range(similarity.shape[0]):
	f.write(samples[i].name)
	for j in range(similarity.shape[1]):
		f.write(','+str(similarity[i][j]))
	f.write("\n")
f.close()