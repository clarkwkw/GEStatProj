import json
import numpy as np
from sklearn.svm import SVR
from sklearn.externals import joblib

def cal_mse(y, y_):
		return np.mean(np.square(y - y_))

class SVM:
	def __init__(self, **kwargs):
		self._trained = False
		self._model = SVR(**kwargs)

	def destroy(self):
		pass

	def train(self, train_matrix, train_labels, valid_matrix, valid_labels, **kwargs):
		if self._trained:
			raise Exception("Model already trained.")
		self._model.fit(train_matrix, train_labels, **kwargs)
		self._trained = True

		valid_pred = self.predict(valid_matrix)
		return cal_mse(valid_pred, valid_labels)

	def predict(self, matrix, **kwargs):
		if not self._trained:
			raise Exception("Model not trained.")
		predictions = self._model.predict(matrix, **kwargs)
		return predictions

	def save(self, savedir):
		if not self._trained:
			raise Exception("Model not trained.")
		joblib.dump(self._model, savedir+'/model.pkl')

	@staticmethod
	def load(savedir):
		model = SimpleSVMModel()
		model._model = joblib.load(savedir+"/model.pkl")
		model._trained = True
		return model