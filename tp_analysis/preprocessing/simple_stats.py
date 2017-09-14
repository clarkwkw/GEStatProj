import numpy as np

def samples_to_dists(samples, classes, get_class):
	class_to_index = {classes[i]: i for i in range(len(classes))}
	dists = np.zeros((len(samples), len(classes)))
	for i in range(len(samples)):
		dists[i, class_to_index[get_class(samples[i])]] = 1
	return dists

def dists_to_labels(dists, classes):
	return np.argmax(dists, axis = 1)

def samples_to_label(samples, classes, get_class):
	class_to_index = {classes[i]: i for i in range(len(classes))}
	dists = np.zeros(len(samples))
	for i in range(len(samples)):
		dists[i] = class_to_index[get_class(samples[i])]
	return dists

def samples_statistics(samples, classes, get_class):
	class_count = {classes[i]: 0 for i in range(len(classes))}
	for sample in samples:
		class_count[get_class(sample)] += 1
	return class_count