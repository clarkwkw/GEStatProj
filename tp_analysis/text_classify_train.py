import filter
import svm
import sample
import os
import preprocessing
import random

_sample_folder = "./samples"
_model_folder = "./models"

_attributes = 50
_normalize = False
_filter_samples = False
_high_portion = 0.15
_low_portion = 0.15
_strategy_parameters = {
	"ngram_rng": (2, 3),
	"selection": "tfidf",
	"words": "samples",
	"use_all": True,
	"ipca_n_attr": 50
}
_svm_parameters = {
}

cross_valid = 5
pca_components = None


def get_label(sample):
	return sample.think + sample.understand + sample.lang + sample.pres

def mkdir(dir):
	try:
		os.mkdir(dir)
	except FileExistsError:
		pass

def main(run = 1, force_run = False):
	if not force_run and len(os.listdir(_model_folder)) > 0:
		ans = input("Found something in '%s', which may be overwitten.\nProceed? [y/n]: "%_model_folder)
		if ans.lower() == 'n':
			exit(-1)
	for k in range(run):
		samples = sample.get_samples(_sample_folder)
		random.shuffle(samples)
		batches = preprocessing.batch_data(samples, cross_valid)
		for i in range(cross_valid):
			valid_samples = batches[i]
			train_samples = []
			
			savedir = "%s/%d/"%(_model_folder, i+1)
			mkdir(savedir)
			for j in range(cross_valid):
				if j != i:
					train_samples.extend(batches[j])
			train_samples, train_labels = filter.score_portion_with_label(train_samples, get_label, _high_portion, _low_portion)
			train_matrix, valid_matrix, words = preprocessing.preprocess(train_samples, valid_samples, normalize_flag = _normalize, savedir = savedir, **_strategy_parameters)
			
			model = svm.SVM()
			model.train(train_matrix, train_labels)
			predictions = model.predict(valid_matrix)
			valid_scores = [get_label(s) for s in valid_samples]
			print("Prediction:")
			print(predictions)
			print("Scores:")
			print(valid_scores)

			model.save(savedir)
			model.destroy()

if __name__ == "__main__":
	main(force_run = True)
