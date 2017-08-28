import numpy as np

def samples_to_dists(samples, classes):
	class_to_index = {classes[i]: i for i in range(len(classes))}
	dists = np.zeros((len(samples), len(classes)))
	for i in range(len(samples)):
		dists[i, class_to_index[samples[i].question]] = 1
	return dists

def dists_to_labels(dists, classes):
	return np.argmax(dists, axis = 1)

def samples_to_label(samples, classes):
	class_to_index = {classes[i]: i for i in range(len(classes))}
	dists = np.zeros(len(samples))
	for i in range(len(samples)):
		dists[i] = class_to_index[samples[i].question]
	return dists

def samples_statistics(samples, classes):
	class_count = {classes[i]: 0 for i in range(len(classes))}
	for sample in samples:
		class_count[sample.question] += 1
	return class_count