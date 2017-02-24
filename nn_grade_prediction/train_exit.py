from neural_network import *

learning_rate = 0.001
training_epocs = 100000
display_step = 100

# No. of hidden units in the second layer
n_hidden_1 = 10

x_titles = ["Logical", "Appreciation of Science", "Understanding of Science", "Understanding of Good life", "Appreciation of Diversity", "Sex", "nSci", "nNonSci", "Eng prof", "Year of Study", "Faculty_Art", "Faculty_Sci", "Faculty_Bus", "cGPA (Before)", "Medium_Can", "Medium_Eng", "Medium_Put", "First GEF", "Q18 (Assigned Text Read)", "Q19 (Chinese Translation)", "Q20 (Text/week)", "Q21 (Time/week)", "Q22 (% Lecture)", "Teacher Number_12", "Teacher Number_17", "Teacher Number_3", "Teacher Number_10", "Teacher Number_18", "Teacher Number_1", "Teacher Number_20", "Teacher Number_13", "Teacher Number_7", "Teacher Number_2", "Teacher Number_15", "Teacher Number_8", "Teacher Number_16", "Teacher Number_9", "Teacher Number_21", "Teacher Number_14", "Teacher Number_22", "Teacher Number_5", "Teacher Number_4", "Teacher Number_19", "Teacher Number_11", "Teacher Number_6"]
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
dataset.init_by_traindata("preprocessed_teacher_UGFN_effort.csv", x_titles, y_title)

# Initialize a neural network with the dataset
nn = Neural_Network(dataset)
nn.configure_parameters(learning_rate, training_epocs, display_step)
nn.configure_network(weights, biases, network)
nn.train()