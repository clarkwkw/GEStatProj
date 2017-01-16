from neural_network import *

learning_rate = 0.001
training_epocs = 100000
display_step = 100
n_hidden_1 = 30

x_titles = ["Q1 (Before)", "Q1 (After)", "Q2 (Before)", "Q2 (After)", "Q3 (Before)", "Q3 (After)", "Q4 (Before)", "Q4 (After)", "Q5 (Before)", "Q5 (After)", "Q6 (Before)", "Q6 (After)", "Q7 (Before)", "Q7 (After)", "Q8 (Before)", "Q8 (After)", "Q9 (Before)", "Q9 (After)", "Q10 (Before)", "Q10 (After)", "Q11 (Before)", "Q11 (After)", "Q12 (Before)", "Q12 (After)", "Q13 (Before)", "Q13 (After)", "Q14 (Before)", "Q14 (After)", "Q15 (Before)", "Q15 (After)", "Q16 (Before)", "Q16 (After)", "Q17 (Before)", "Q17 (After)", "Q18 (0-1)", "Q18 (2-3)", "Q18 (4-5)", "Q18 (6-7)", "Q18 (8-9)", "Q18 (10-11)", "Q18 (12)", "Q19 (0-1)", "Q19 (2-3)", "Q19 (4-5)", "Q19 (6-7)", "Q19 (8-9)", "Q19 (10-11)", "Q20 (0%)", "Q20 (1 to 20%)", "Q20 (21 to 40%)", "Q20 (41 to 60%)", "Q20 (61 to 80 %)", "Q20 (81 to 100%)", "Q21 (less than 1)", "Q21 (1 to < 2hrs)", "Q21 (2 to <3hrs)", "Q21 (3 to <4hrs)", "Q21 (more than 4)", "Q22 (0%)", "Q22 (1 to 20%)", "Q22 (21 to 40%)", "Q22 (41 to 60%)", "Q22 (61 to 80 %)", "Q22 (81 to 100%)", "Sex", "Phy", "Chem", "Bio", "Com Sci", "Inter Sci", "Eng Lit", "Chin Lit", "History", "Chin History", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog", "Lang_Cant", "Lang_Put", "Lang_Other", "DSE?", "DSE Eng Grade", "Understanding - Lecture1", "Understanding - Lecture2", "Understanding - Lecture3", "Understanding - Tutorial1", "Understanding - Tutorial2", "Understanding - Tutorial3", "Understanding - Tutorial4", "Understanding - Tutorial5", "Understanding - Tutorial6", "Understanding - Outside Class1", "Understanding - Outside Class2", "Understanding - Outside Class3", "Understanding - Outside Class4", "Interesting - Lecture1", "Interesting - Lecture2", "Interesting - Lecture3", "Interesting - tutorial1", "Interesting - tutorial2", "Interesting - tutorial3", "Interesting - tutorial4", "Interesting - tutorial5", "Interesting - tutorial6", "Intersting - Outside Class1", "Intersting - Outside Class2", "Intersting - Outside Class3", "Intersting - Outside Class4", "Time - Lecture1", "Time - Lecture2", "Time - Lecture3", "Time - Tutorial1", "Time - Tutorial2", "Time - Tutorial3", "Time - Tutorial4", "Time - Tutorial5", "Time - Tutorial6", "Year of Study", "Faculty_ART", "Faculty_BAF", "Faculty_BASCI", "Faculty_BASSF", "Faculty_CCST", "Faculty_EDU", "Faculty_ENF", "Faculty_ENSCF", "Faculty_MED", "Faculty_SCF", "Faculty_SLAW", "Faculty_SSF", "cGPA (Before)", "First GEF?"]

def network(x, weights, biases):
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.sigmoid(layer_1)
	out_layer = tf.add(tf.matmul(layer_1, weights['out']), biases['out'])
	return out_layer

weights = {
    'h1': tf.Variable(tf.random_normal([len(x_titles), n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 5]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([5]))
}

dataset = Dataset()
dataset.init_by_testdata("processed.csv", x_titles)
nn = Neural_Network(dataset)
nn.configure_parameters(learning_rate, training_epocs, display_step)
nn.configure_network(weights, biases, network)
result = nn.test("exit_6507/")
for x in result:
	print x[0]