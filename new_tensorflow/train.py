import numpy as np
import tensorflow as tf
from timeit import default_timer

print "Loading Data..."
data = np.loadtxt('../ml_data_generation/data.txt')
print "Data Loaded"
batch_size = 5000
num_epochs = 500000
accuracy_print_rate = 10

X_train= data[:,:18]
y_train = data[:, 18:]

np.random.shuffle(X_train)
np.random.shuffle(y_train)

X_batches = []
y_batches = []

last_index = 0
for i in xrange(0, X_train.shape[0], batch_size):
    X_batches.append(X_train[i: i + batch_size])
    y_batches.append(y_train[i: i + batch_size])
    last_index = i

if X_train.shape[0] % batch_size != 0:
    X_batches.append(X_train[last_index:])
    y_batches.append(y_train[last_index:])

num_batches = len(X_batches)

W = {}
b = {}


def model(X, nodes):
    layers = {}
    layers_compute = {}
    for i in range(1, len(nodes)):
        print i
        new_layer = {'weights': tf.Variable(tf.random_normal([nodes[i - 1], nodes[i]], 0, 0.1)),
                     'biases': tf.Variable(tf.random_normal([nodes[i]], 0, 0.1))}
        layers[i - 1] = new_layer

        l = tf.matmul(X if i == 1 else layers_compute[i - 2], layers[i - 1]['weights'])

        l = tf.nn.relu(l) if i != len(nodes) - 1 else tf.nn.softmax(l)

        layers_compute[i - 1] = l

    return layers_compute[len(layers_compute) - 1]


X = tf.placeholder(tf.float32, [None, 18])
y = tf.placeholder(tf.float32, [None, 3])
nodes = [18, 10, 10, 3]

predictions = model(X, nodes)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predictions, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=0.002).minimize(cost)
correct_prediction = tf.equal(y, tf.round(predictions))


with tf.Session() as sess:
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    for epoch in xrange(num_epochs):
        start = default_timer()
        total_cost = 0
        total_accuracy = 0
        for batch in xrange(num_batches):
            _, c = sess.run([optimizer, cost], feed_dict={X : X_batches[batch], y: y_batches[batch]})
            # print "Batch Cost: {0}".format(c)
            total_cost += c
            if epoch % accuracy_print_rate == 0:
                total_accuracy += sess.run(tf.reduce_mean(tf.cast(correct_prediction, tf.float32)), feed_dict={X : X_batches[batch], y: y_batches[batch]})
        end = default_timer()
        if epoch % accuracy_print_rate == 0:
            print "Epoch: {0} Time {1} Cost: {2} Accuracy: {3}%".format(epoch, end - start, total_cost / num_batches, total_accuracy / num_batches * 100)
        # else:
        #     print "Epoch: {0} Time {1}s Cost: {2}".format(epoch, end - start, totalCost / num_batches)
        save_path = saver.save(sess, "weights/weights.ckpt")


