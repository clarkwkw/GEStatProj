from neural_network import *

learning_rate = 0.001
training_epocs = 100000
display_step = 100
n_hidden_1 = 10

x_titles = ["Logical", "Appreciation of Science", "Understanding of Science", "Understanding of Good life", "Appreciation of Diversity", "Sex", "nSci", "nNonSci", "Eng prof", "Year of Study", "Faculty_Art", "Faculty_Sci", "Faculty_Bus", "cGPA (Before)", "Medium_Can", "Medium_Eng", "Medium_Put", "First GEF", "Q18 (Assigned Text Read)", "Q19 (Chinese Translation)", "Q20 (Text/week)", "Q21 (Time/week)", "Q22 (% Lecture)"]
y_title = "Grade_dec"

def network(x, weights, biases):
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	out_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])
	return out_layer

weights = {
    'h1': tf.Variable(tf.random_normal([len(x_titles), n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 1]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([1]))
}

dataset = Dataset()
dataset.init_by_testdata("preprocessed_witheffort_UGFN.csv", x_titles)
nn = Neural_Network(dataset)
nn.configure_parameters(learning_rate, training_epocs, display_step)
nn.configure_network(weights, biases, network)

# Specify the path to checkpoint file (saved model) here
result = nn.test("exit1448/")
for x in result:
	print x[0]