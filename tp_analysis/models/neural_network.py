import json
import numpy as np
import sys
import signal
import tensorflow as tf
from . import utils

_multi_thread = 8
_forced_quit = False

def cal_mse(y, y_):
	return np.mean(np.square(y - y_))

def cal_cross_entropy(predict, real):
	return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real, logits=predict))

class Neural_Network:
	def __init__(self, _n_factors = None, _hidden_nodes = [], _last_layer = 1, _learning_rate = 0.001, from_save = None):
		self._hidden_nodes = _hidden_nodes
		self._last_layer = _last_layer
		self._weights = []
		self._biases = []		
		self._learning_rate = _learning_rate
		self._n_factors = _n_factors
		self._trained = False
		self._graph = tf.Graph()
		self._sess = tf.Session(graph = self._graph, config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread))
		with self._graph.as_default() as g:
			if from_save is None:
				n_last_layer = _n_factors
				n_next_layer = 0
				for i in range(0, len(_hidden_nodes) + 1):
					if i >= len(_hidden_nodes):
						n_next_layer = _last_layer
					else:
						n_next_layer = _hidden_nodes[i]
					self._weights.append(tf.get_variable("w_"+str(i), initializer = tf.random_normal([n_last_layer, n_next_layer])))
					self._biases.append(tf.get_variable("b_"+str(i), initializer = tf.random_normal([n_next_layer])))
					if i < len(_hidden_nodes):
						n_last_layer = _hidden_nodes[i]
				self._X = tf.placeholder(tf.float32, [None, _n_factors], name = "X")
				self._pred = self.__network(self._X)
				tf.add_to_collection("pred", self._pred)
				if _last_layer == 1:
					self._y = tf.placeholder(tf.float32, [None], name = "y")
					self._cost = tf.reduce_mean(tf.square(self._pred - self._y))
				else:
					self._y = tf.placeholder(tf.float32, [None, _last_layer], name = "y")
					self._cost = cal_cross_entropy(self._pred, self._y)
				self._optimizer = tf.train.AdamOptimizer(self._learning_rate).minimize(self._cost)
				init = tf.global_variables_initializer()
				self._sess.run(init)	
			else:
				saver = tf.train.import_meta_graph(from_save+'/model.ckpt.meta')
				saver.restore(self._sess, from_save+'/model.ckpt')
				self._X = g.get_tensor_by_name("X:0")
				self._y = g.get_tensor_by_name("y:0")
				self._pred =  tf.get_collection("pred")[0]
				self._trained = True
		tf.reset_default_graph()

	def destroy(self):
		self._sess.close()

	def train(self, train_matrix, train_labels, valid_matrix = None, valid_labels = None, adaptive = True, step = 300, max_iter = 10000):
		if self._trained:
			raise Exception("Model already trained.")
		valid_cost = None
		with self._graph.as_default() as g:
			decider = None
			if adaptive:
				decider = Train_decider()
			for i in range(max_iter):
				_, train_cost = self._sess.run([self._optimizer, self._cost], feed_dict = {self._X: train_matrix, self._y: train_labels})
				if adaptive and (i+1)%step == 0:
					valid_predict = self._pred.eval(feed_dict = {self._X: valid_matrix}, session = self._sess)
					if self._last_layer == 1:
						valid_cost = cal_mse(valid_predict, valid_labels)
					else:
						valid_cost = cal_cross_entropy(valid_predict, valid_labels).eval(session = self._sess)
					#print("Epoch %5d: %.4f"%(i+1, valid_cost))
					if decider.update(valid_cost) == False:
						break
			if adaptive:
				valid_predict = self._pred.eval(feed_dict = {self._X: valid_matrix}, session = self._sess)
				if self._last_layer == 1:
					valid_cost = cal_mse(valid_predict, valid_labels)
				else:
					valid_cost = cal_cross_entropy(valid_predict, valid_labels).eval(session = self._sess)

		tf.reset_default_graph()
		self._trained = True
		if adaptive:
			return valid_cost

	def predict(self, matrix):
		if not self._trained:
			raise Exception("Model not trained.")
		with self._graph.as_default() as g:
			tmp_result = self._sess.run(self._pred, feed_dict = {self._X: matrix})
		tf.reset_default_graph()
		if self._last_layer == 1:
			return [y[0] for y in tmp_result]
		else:
			return tmp_result

	def __network(self, X):
		tmp_result = X
		for i in range(len(self._hidden_nodes) + 1):
			tmp_result = tf.add(tf.matmul(tmp_result, self._weights[i]), self._biases[i])
			if i < len(self._hidden_nodes):
				tmp_result = tf.nn.sigmoid(tmp_result)
		return tmp_result

	def save(self, savedir):
		if not self._trained:
			raise Exception("Model not trained.")
		utils.ensure_dir_exist(savedir)
		with self._graph.as_default() as g:
			saver = tf.train.Saver()
			save_path = saver.save(self._sess, save_path = savedir+'/model.ckpt')
		tf.reset_default_graph()
		with open(savedir+"/model_conf.json", "w") as f:
			init_para = {
				"_n_factors": self._n_factors,
				"_hidden_nodes": self._hidden_nodes,
				"_last_layer": self._last_layer
			}
			f.write(json.dumps(init_para, indent = 4))

	@staticmethod
	def load(savedir):
		init_para = None
		with open(savedir+"/model_conf.json", "r") as f:
			init_para = json.load(f)
		model = Neural_Network(from_save = savedir, **init_para)
		model._trained = True
		return model

class Train_decider:
	tolerance = 2

	def __init__(self):
		self.cost_initialized = False
		self.cont = True
		self.count = 0
	
	# Given a error cost, compare it with the previous one, if it keeps increasing for certain no. of epochs, return False.
	# Otherwise, return True
	def update(self, cost):
		if _forced_quit:
			return False
		if self.cost_initialized == False:
			self.prev_cost = cost
			self.cost_initialized = True
			self.cont = True
			self.count = 0
		else:
			if cost > self.prev_cost:
				self.count = self.count + 1
			else:
				self.count = 0
			self.prev_cost = cost
			self.cont = self.count <= Train_decider.tolerance
		return self.cont

	def cont(self):
		if _forced_quit:
			return False
		return self.cont

def signal_handler(signal, frame):
	print("Quit signal received. Please wait...")
	global _forced_quit
	_forced_quit = True