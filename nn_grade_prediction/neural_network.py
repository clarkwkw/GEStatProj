import csv
import numpy as np
import tensorflow as tf
import random
import sys
import signal

_forced_quit = False
_multi_thread = 10
_cross_validation = 10

def cal_accuracy(y, y_):
		return np.mean(np.argmax(y, 1) == np.argmax(y_, 1))

def vect_to_grade(vect):
	grades = ["A", "B", "C", "D", "F"]
	tmp = np.argmax(vect, 1)
	return [grades[x] for x in tmp]

class Dataset:
	def init_by_traindata(self, csv_path, x_titles, y_title):
		self.x_titles = x_titles
		self.y_title = y_title

		file = open(csv_path, 'r')
		tmp_X = [ [] for i in range(len(x_titles))]
		tmp_Y = []
		for row in csv.DictReader(file):
			for i in range(len(x_titles)):
				tmp_X[i].append(row[x_titles[i]])

			# A, B, C, D, F
			new_y = np.zeros(5)
			if row[y_title] == "A":
				new_y[0] = 1
			elif row[y_title] == "B":
				new_y[1] = 1
			elif row[y_title] == "C":
				new_y[2] = 1
			elif row[y_title] == "D":
				new_y[3] = 1
			else:
				new_y[4] = 1
			tmp_Y.append(new_y)
		file.close()

		tmp_X = np.asarray(tmp_X, dtype = np.float32)
		tmp_Y = np.asarray(tmp_Y, dtype = np.float32)

		self.m = len(tmp_X[0])

		self.X = np.transpose(tmp_X)
		self.Y = tmp_Y

	def init_by_testdata(self, csv_path, x_titles):
		self.x_titles = x_titles
		file = open(csv_path, 'r')
		tmp_X = [ [] for i in range(len(x_titles))]
		for row in csv.DictReader(file):
			for i in range(len(x_titles)):
				tmp_X[i].append(row[x_titles[i]])
		file.close()

		tmp_X = np.asarray(tmp_X, dtype = np.float32)

		self.m = len(tmp_X[0])

		self.X = np.transpose(tmp_X)

	def fold_partition(self, fold_count):
		self.sample_sequence = random.sample(range(self.m), self.m)
		self.test_fold = (0, self.m/fold_count)
		train_fold = [x for x in range(0, self.m) if x not in self.sample_sequence[self.test_fold[0]:self.test_fold[1]]]
		return (self.sample_sequence[self.test_fold[0]:self.test_fold[1]], train_fold)

	def next_fold(self):
		self.test_fold = (self.test_fold[1]%self.m, (self.test_fold[1]*2-self.test_fold[0])%self.m)
		train_fold = [x for x in range(0, self.m) if x not in self.sample_sequence[self.test_fold[0]:self.test_fold[1]]]
		return (self.sample_sequence[self.test_fold[0]:self.test_fold[1]], train_fold)

class Neural_Network:
	def __init__(self, dataset):
		self.dataset = dataset

	def configure_parameters(self, learning_rate, training_epocs, display_step):
		self.learning_rate = learning_rate
		self.training_epocs = training_epocs
		self.display_step = display_step

	def configure_network(self, weights, biases, network):
		self.weights = weights
		self.biases = biases
		self.network = network

	def train(self):

		X = tf.placeholder(tf.float32, [None, len(self.dataset.x_titles)])
		Y = tf.placeholder(tf.float32, [None, 5])

		pred = self.network(X, self.weights, self.biases)
		cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, Y))

		optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(cross_entropy)
		train_prediction = tf.nn.softmax(Y)

		init = tf.initialize_all_variables()

		test_set, train_set = self.dataset.fold_partition(_cross_validation)

		
		signal.signal(signal.SIGINT, signal_handler)

		max_accuracy = 0
		global_accuracy = []
		for fold_no in range(_cross_validation):
			print "Fold", (fold_no+1), ":",
			sys.stdout.flush()
			decider = Train_decider()
			with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread)) as sess:
				sess.run(init)
				for epoch in range(self.training_epocs):
					_, c = sess.run([optimizer, cross_entropy], feed_dict = {X: self.dataset.X[train_set], Y: self.dataset.Y[train_set]})
					if epoch % self.display_step == 0:
						#print "Epoch:", "%06d" % (epoch+1), "Entropy =", "%.4f" % (c)
						test_c, test_pred = sess.run([cross_entropy, pred], feed_dict = {X: self.dataset.X[test_set], Y: self.dataset.Y[test_set]})
						test_accuracy = cal_accuracy(test_pred, self.dataset.Y[test_set])
						#print "=====> Test Entropy =", "%.4f" % test_c, "Test Accuracy =", "%.4f" % test_accuracy
						if decider.update(test_c) == False:
							break
				test_pred = pred.eval(feed_dict = {X: self.dataset.X[test_set]}, session = sess)
				test_accuracy = cal_accuracy(test_pred, self.dataset.Y[test_set])
				print test_accuracy
				global_accuracy.append(test_accuracy)
				if test_accuracy > max_accuracy:
					max_accuracy = test_accuracy
					saver = tf.train.Saver()
					saver.save(sess, "Tmp.ckpt", global_step = 1)
			if _forced_quit:
				break;
			test_set, train_set = self.dataset.next_fold()
		global_accuracy = np.asarray(global_accuracy)
		print "Max accuracy:", "%.4f" % max_accuracy, "Averge accuracy:", "%.4f" % np.mean(global_accuracy), "Variance:", "%.4f" % np.var(global_accuracy)
		print "Accuracy Vector:"
		print global_accuracy
		signal.signal(signal.SIGINT, signal.SIG_DFL)

	def test(self, save_path):
		X = tf.placeholder(tf.float32, [None, len(self.dataset.x_titles)])
		pred = self.network(X, self.weights, self.biases)
		saver = tf.train.Saver()
		init = tf.initialize_all_variables()

		signal.signal(signal.SIGINT, signal.SIG_IGN)
		result = []
		with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread)) as sess:
			sess.run(init)
			ckpt = tf.train.get_checkpoint_state(save_path)
			if ckpt and ckpt.model_checkpoint_path:
				saver.restore(sess, ckpt.model_checkpoint_path)
			else:
				print "Check point file not found. Exit."
				sys.exit(0)
			result = pred.eval(feed_dict = {X: self.dataset.X}, session = sess)
			result = vect_to_grade(result)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		return result

class Train_decider:
	tolerance = 2
	def __init__(self):
		self.cost_initialized = False
		self.cont = True
		self.count = 0
		
	def update(self, cost):
		if _forced_quit:
			return False
		if self.cost_initialized == False:
			self.prev_cost = cost
			self.cost_initialized = True
			self.cont = True
			self.count = 0
		else:
			self.count += (cost - self.prev_cost) > 0
			self.prev_cost = cost
			self.cont = self.count <= Train_decider.tolerance

		return self.cont

	def cont(self):
		if _forced_quit:
			return False
		return self.cont

def signal_handler(signal, frame):
	print "Quit signal received. Please wait..."
	global _forced_quit
	_forced_quit = True
