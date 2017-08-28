import math
import numpy as np

def score_portion(samples, get_score, high_portion, low_portion, separate = False):
	n_high, n_low = None, None
	n_samples = len(samples)
	if high_portion + low_portion > 1:
		raise Exception("sum of low_portion and high_portion can not exceed 1")
	n_high = math.floor(n_samples*high_portion)
	n_low = math.ceil(n_samples*low_portion)

	sorted_sample_tups = [(sample, get_score(sample)) for sample in samples]
	sorted_sample_tups = sorted(sorted_sample_tups, key = lambda x: x[1])
	selected_samples_low = [t[0] for t in sorted_sample_tups[0:n_low]]
	selected_samples_high = [t[0] for t in sorted_sample_tups[(n_samples - n_high):n_samples]]
	if not separate:
		return  selected_samples_high + selected_samples_low
	else:
		return selected_samples_high, selected_samples_low

def score_portion_with_label(samples, get_score, high_portion, low_portion):
	high_samples, low_samples = score_portion(samples, get_score, high_portion, low_portion, True)

	labels = np.zeros(len(high_samples) + len(low_samples))
	labels[0:len(high_samples)] = 1

	return high_samples + low_samples, labels