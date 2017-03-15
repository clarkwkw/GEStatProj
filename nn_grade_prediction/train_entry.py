from neural_network import *

learning_rate = 0.001
training_epocs = 100000
display_step = 100

# No. of hidden units in the second layer
n_hidden_1 = 10

x_titles = ["Logical", "Appreciation of Science", "Understanding of Science", "Understanding of Good life", "Appreciation of Diversity", "Sex", "nSci", "nNonSci", "Eng prof", "Year of Study", "Faculty_Art", "Faculty_Sci", "Faculty_Bus", "cGPA (Before)", "First GEF"]
y_title = "Grade_dec"


# Define the network structure
def network(x, weights, biases):
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	out_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])
	return out_layer

# Define the weight variables
weights = {
    'h1': tf.Variable(tf.random_normal([len(x_titles), n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 1]))
}

# Define the bias variables
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([1]))
}

# Import csv file
dataset = Dataset()
dataset.init_by_traindata("preprocessed.csv", x_titles, y_title)

# Initialize a neural network with the dataset
nn = Neural_Network(dataset)
nn.configure_parameters(learning_rate, training_epocs, display_step)
nn.configure_network(weights, biases, network)
nn.train(True)