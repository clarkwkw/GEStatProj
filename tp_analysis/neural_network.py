import numpy as np
import sys
import signal
import tensorflow as tf
import visualization as vis

_multi_thread = 4
_forced_quit = False

def cal_mse(y, y_):
		return np.mean(np.square(y - y_))

class Neural_Network:

	def configure_parameters(self, learning_rate, training_epocs, display_step):
		self.learning_rate = learning_rate
		self.training_epocs = training_epocs
		self.display_step = display_step

	def configure_network(self, weights, biases, network):
		self.weights = weights
		self.biases = biases
		self.network = lambda x: network(x, self.weights, self.biases)

	def train(self, train_samples_matrix, train_labels, valid_samples_matrix, valid_labels, save_name, visualize = False):
		saver = tf.train.Saver()
		X = tf.placeholder(tf.float32, [None, train_samples_matrix.shape[1]])
		Y = tf.placeholder(tf.float32, [None, ])
		pred = self.network(X)
		mse = tf.reduce_mean(tf.square(pred - Y))
		optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(mse)

		signal.signal(signal.SIGINT, signal_handler)

		tf_version = float(tf.__version__[0:3])
		init = 0
		if tf_version < 1:
			init = tf.initialize_all_variables()
		else:
			init = tf.global_variables_initializer()
		sess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread))
		sess.run(init)
		decider = Train_decider()
		if visualize:
			mse_plot = vis.MSEPlot()

		for epoch in range(self.training_epocs):
			_, c = sess.run([optimizer, mse], feed_dict = {X: train_samples_matrix, Y: train_labels})
			if epoch % self.display_step == 0:
				valid_pred = sess.run([pred], feed_dict = {X: valid_samples_matrix})
				valid_mse = cal_mse(valid_pred, valid_labels)
				if visualize:
					mse_plot.add_point(epoch, valid_mse, 1)
					mse_plot.add_point(epoch, c, 0)
				if decider.update(valid_mse) == False:
					break

		valid_pred = sess.run([pred], feed_dict = {X: valid_samples_matrix})
		valid_mse = cal_mse(valid_pred, valid_labels)
		if visualize:
			mse_plot.show()
		
		saver.save(sess, save_name+"model.ckpt")

		signal.signal(signal.SIGINT, signal.SIG_DFL)
		return(valid_mse)

	def test(self, test_samples_matrix, save_path):
		saver = tf.train.Saver()
		X = tf.placeholder(tf.float32, [None, test_samples_matrix.shape[1]])
		Y = tf.placeholder(tf.float32, [None, ])
		pred = self.network(X)
		tf_version = float(tf.__version__[0:3])
		init = 0
		if tf_version < 1:
			init = tf.initialize_all_variables()
		else:
			init = tf.global_variables_initializer()
		sess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread))
		sess.run(init)
		ckpt = tf.train.get_checkpoint_state(save_path)
		if ckpt and ckpt.model_checkpoint_path:
			saver.restore(sess, ckpt.model_checkpoint_path)
		else:
			print ("Check point file not found. Exit.")
			return []
		test_pred = pred.eval(feed_dict = {X: test_samples_matrix}, session = sess)
		return [y[0] for y in test_pred]

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
		return True
		if _forced_quit:
			return False
		return self.cont

def signal_handler(signal, frame):
	print("Quit signal received. Please wait...")
	global _forced_quit
	_forced_quit = True