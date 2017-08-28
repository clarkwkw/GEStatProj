import os
import numpy as np
import preprocessing
import textbook
import nltk
import pandas

sample_folder = "./samples"
out_file = "similarity.csv"
n_key_vocabs = 30

samples = preprocessing.tp_sample.get_samples(sample_folder)
samples_textbook = [sample.text for sample in samples]+textbook.getOrderedText()
vectorizer = textbook.getTfidfVectorizer()
tfidf = vectorizer.transform(samples_textbook)
similarity = (tfidf*tfidf.T).A
similarity = similarity[0:len(samples), len(samples):]

similarity_df = pandas.DataFrame(similarity, columns = textbook.getChapterTitles())
similarity_df.index = [sample.get_identifier() for sample in samples]

similarity_df.to_csv(out_file)
