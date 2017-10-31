import json
import numpy as np
import sklearn.svm as sk_svm
from sklearn.externals import joblib
from . import utils

def cal_mse(y, y_):
		return np.mean(np.square(y - y_))

class SVR:
	def __init__(self, **kwargs):
		self._trained = False
		self._model = sk_svm.SVR(**kwargs)

	def destroy(self):
		pass

	def train(self, train_matrix, train_labels, valid_matrix = None, valid_labels = None, **kwargs):
		if self._trained:
			raise Exception("Model already trained.")
		self._model.fit(train_matrix, train_labels, **kwargs)
		self._trained = True

		if valid_matrix is not None and valid_labels is not None:
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
		utils.ensure_dir_exist(savedir)
		joblib.dump(self._model, savedir+'/model.pkl')

	@staticmethod
	def load(savedir):
		model = SVR()
		model._model = joblib.load(savedir+"/model.pkl")
		model._trained = True
		return model

class SVM:
	def __init__(self, **kwargs):
		self._trained = False
		self._model = sk_svm.SVC(**kwargs)

	def destroy(self):
		pass

	def train(self, train_matrix, train_labels, **kwargs):
		if self._trained:
			raise Exception("Model already trained.")
		self._model.fit(train_matrix, train_labels, **kwargs)
		self._trained = True

	def predict(self, matrix, **kwargs):
		if not self._trained:
			raise Exception("Model not trained.")
		predictions = self._model.predict(matrix, **kwargs)
		return predictions

	def save(self, savedir):
		if not self._trained:
			raise Exception("Model not trained.")
		utils.ensure_dir_exist(savedir)
		joblib.dump(self._model, savedir+'/model.pkl')

	@staticmethod
	def load(savedir):
		model = SVM()
		model._model = joblib.load(savedir+"/model.pkl")
		model._trained = True
		return model