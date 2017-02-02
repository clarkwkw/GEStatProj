'''
This file defines:
1. The way to import csv files (Dataset class)
2. The way to train neural network (Neural_Network class)
3. When to stop training (Train_decider class)
4. Other utilities functions
'''

import csv
import numpy as np
import tensorflow as tf
import random
import sys
import signal

_forced_quit = False


# No. of threads to be used when training and testing
_multi_thread = 10

# No. of cross validation needs to be performed
_cross_validation = 10

# Calculate mean square error between predicted values and true values
def cal_mse(y, y_):
		return np.mean(np.square(y - y_))

class Dataset:

	# Initialize the data set by training data: x, y values known
	# csv_path: path to pre-processed csv file
	# x_titles: list of column names of x
	# y_title: a string of column name of y
	def init_by_traindata(self, csv_path, x_titles, y_title):
		self.x_titles = x_titles
		self.y_title = y_title

		file = open(csv_path, 'r')

		# Initialize a matrix for storing x values
		tmp_X = [ [] for i in range(len(x_titles))]

		# Initialize a matrix for storing y values
		tmp_Y = []

		# Iterate over each row of the csv file, and put the values into the matrices
		for row in csv.DictReader(file):
			for i in range(len(x_titles)):
				tmp_X[i].append(row[x_titles[i]])
			tmp_Y.append([row[y_title]])

		file.close()

		# Convert the matrices into numpy array structure (easier to compute)
		tmp_X = np.asarray(tmp_X, dtype = np.float32)
		tmp_Y = np.asarray(tmp_Y, dtype = np.float32)

		# Record the no. of rows
		self.m = len(tmp_X[0])

		self.X = np.transpose(tmp_X)
		self.Y = tmp_Y

	# Initialize the data set by testing data: x value known
	# csv_path: path to pre-processed csv file
	# x_titles: list of column names of x
	# This function does almost the same as the previous function, but without importing any y value
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

	# This function shuffle the data and return the first partition
	# fold_count: no. of folds needs to be performed in cross validation
	def fold_partition(self, fold_count):
		# Shuffle
		self.sample_sequence = random.sample(range(self.m), self.m)

		# Store the tuple of starting and ending index of testing data
		self.test_fold = (0, self.m/fold_count)

		# Find out the remaining indices, those are for training
		train_fold = [x for x in range(0, self.m) if x not in self.sample_sequence[self.test_fold[0]:self.test_fold[1]]]
		
		# Return indices of testing data and training data in a tuple
		return (self.sample_sequence[self.test_fold[0]:self.test_fold[1]], train_fold)

	# This function returns the indices of the next fold of data
	def next_fold(self):

		# Calulate the indices of the next fold of testing data
		self.test_fold = (self.test_fold[1], self.test_fold[1]*2-self.test_fold[0])

		# Find out the remaining data, they are the training data
		train_fold = [x for x in range(0, self.m) if x not in self.sample_sequence[self.test_fold[0]:self.test_fold[1]]]

		# Put both of them into a tuple
		return (self.sample_sequence[self.test_fold[0]:self.test_fold[1]], train_fold)

class Neural_Network:

	# Initialize the network by giving a dataset object
	def __init__(self, dataset):
		self.dataset = dataset

	# Configure some training parameters, they are floating point numbers
	# training_epocs: max. no. of "rounds" to be used to train
	# display_step: no. of "rounds" to display intermediate progress
	def configure_parameters(self, learning_rate, training_epocs, display_step):
		self.learning_rate = learning_rate
		self.training_epocs = training_epocs
		self.display_step = display_step

	# Configure the network with weights, biases and network structure
	def configure_network(self, weights, biases, network):
		self.weights = weights
		self.biases = biases
		self.network = network

	def train(self):
		# The following is just some definition for Tensorflow library, the training has not started yet

		# Placeholders for the network required by the Tensorflow library
		# The structure of X is [ , no. of independent variables] 
		# The structure of Y is [ , no. of categories for dependent variables]
		#  (Note that the first dimension is not fixed since the no. of records can vary)
		X = tf.placeholder(tf.float32, [None, len(self.dataset.x_titles)])
		Y = tf.placeholder(tf.float32, [None, 1])

		# Let the library know that we are going to put X into designed network
		pred = self.network(X, self.weights, self.biases)

		# The equation to evaluate the prediction of the network
		mse = tf.reduce_mean(tf.square(pred - Y))

		# The library should improve the network according to mean square error
		optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(mse)

		# Set up an initializer for the above variables/ placeholders
		init = tf.initialize_all_variables()

		# Obtain the first fold of training and testing data
		test_set, train_set = self.dataset.fold_partition(_cross_validation)

		signal.signal(signal.SIGINT, signal_handler)

		min_mse = float("inf")
		global_mse = []

		# Starting training with cross validation
		for fold_no in range(_cross_validation):

			print "Fold", (fold_no+1), ":",
			sys.stdout.flush()

			# Initialize a decider object to check when to stop training
			decider = Train_decider()


			with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread)) as sess:
				sess.run(init)

				for epoch in range(self.training_epocs):

					# Run the defined optimizer with training data & testing data
					_, c = sess.run([optimizer, mse], feed_dict = {X: self.dataset.X[train_set], Y: self.dataset.Y[train_set]})
					
					# It is time to display progress and evluate the network
					if epoch % self.display_step == 0:
						#print "Epoch:", "%06d" % (epoch+1), "MSE =", "%.4f" % (c)
						
						# Calculate the mse on testing data
						test_pred = sess.run([pred], feed_dict = {X: self.dataset.X[test_set]})
						test_mse = cal_mse(test_pred, self.dataset.Y[test_set])
						#print "=====> Test MSE =", "%.4f" % test_mse
						
						# Let the decider know the current testing mse
						if decider.update(test_mse) == False:
							break

				# Training for one fold is over, calculate the final testing mse
				test_pred = pred.eval(feed_dict = {X: self.dataset.X[test_set]}, session = sess)

				test_mse = cal_mse(test_pred, self.dataset.Y[test_set])
				print test_mse

				# Save the error. If this is the lowest so far, also save the network configuration
				global_mse.append(test_mse)
				if test_mse < min_mse:
					min_mse = test_mse
					saver = tf.train.Saver()
					saver.save(sess, "Tmp.ckpt", global_step = 1)
			if _forced_quit:
				break;

			# Get the next fold of data
			test_set, train_set = self.dataset.next_fold()



		# All folds are over, output the training statistics
		global_mse = np.asarray(global_mse)
		print "Min MSE:", "%.4f" % min_mse, "Averge MSE:", "%.4f" % np.mean(global_mse), "Variance:", "%.4f" % np.var(global_mse)
		print "MSE Vector:"
		print global_mse
		signal.signal(signal.SIGINT, signal.SIG_DFL)

	# This is for prediction
	# save_path: The path to a folder containing the save file
	def test(self, save_path):

		# Again, some defintion for Tensorflow
		X = tf.placeholder(tf.float32, [None, len(self.dataset.x_titles)])
		pred = self.network(X, self.weights, self.biases)
		saver = tf.train.Saver()
		init = tf.initialize_all_variables()

		signal.signal(signal.SIGINT, signal.SIG_IGN)
		result = []

		# Predict
		with tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads = _multi_thread)) as sess:
			sess.run(init)

			# Load the save file
			ckpt = tf.train.get_checkpoint_state(save_path)
			if ckpt and ckpt.model_checkpoint_path:
				saver.restore(sess, ckpt.model_checkpoint_path)
			else:
				print "Check point file not found. Exit."
				sys.exit(0)

			# Feed the x values and get prediction
			result = pred.eval(feed_dict = {X: self.dataset.X}, session = sess)
			self.printPar(sess)

		signal.signal(signal.SIGINT, signal.SIG_DFL)
		return result

	# Print the weights and biases	
	def printPar(self, sess):
		print "Weights: "
		for (key, value) in self.weights.items():
			print "\t"+key+": "
			print sess.run(value)
		print "Biases: "
		for (key, value) in self.weights.items():
			print "\t"+key+": "

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
	print "Quit signal received. Please wait..."
	global _forced_quit
	_forced_quit = True
