from neural_network import *

learning_rate = 0.001
training_epocs = 100000
display_step = 100

# No. of hidden units in the second layer
n_hidden_1 = 20

x_titles = ["Q1 (Before)", "Q2 (Before)", "Q3 (Before)", "Q4 (Before)", "Q5 (Before)", "Q6 (Before)", "Q7 (Before)", "Q8 (Before)", "Q9 (Before)", "Q10 (Before)", "Q11 (Before)", "Q12 (Before)", "Q13 (Before)", "Q14 (Before)", "Q15 (Before)", "Q16 (Before)", "Q17 (Before)", "Sex", "Phy", "Chem", "Bio", "Com Sci", "Inter Sci", "Eng Lit", "Chin Lit", "History", "Chin History", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog", "Lang_Cant", "Lang_Put", "Lang_Other", "DSE?", "DSE Eng Grade", "Year of Study", "Faculty_ART", "Faculty_BAF", "Faculty_BASCI", "Faculty_BASSF", "Faculty_CCST", "Faculty_EDU", "Faculty_ENF", "Faculty_ENSCF", "Faculty_MED", "Faculty_SCF", "Faculty_SLAW", "Faculty_SSF", "cGPA (Before)", "First GEF?"]
y_title = "Grade Catagorised"


# Define the network structure
def network(x, weights, biases):
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	out_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])
	return out_layer

# Define the weight variables
weights = {
    'h1': tf.Variable(tf.random_normal([len(x_titles), n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 5]))
}

# Define the bias variables
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([5]))
}

# Import csv file
dataset = Dataset()
dataset.init_by_traindata("processed.csv", x_titles, y_title)

# Initialize a neural network with the dataset
nn = Neural_Network(dataset)
nn.configure_parameters(learning_rate, training_epocs, display_step)
nn.configure_network(weights, biases, network)
nn.train()