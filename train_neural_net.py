import numpy as np
from scipy.optimize import fmin_cg
import sys
from numba import jit
import threading

#12m0.816s runtime on first train (5 hidden layers)
#12m32.046s runtime on second train (10 hidden layers)
backprop_iter = 0

#data loading
datafile = open('data.txt')
raw_data = np.loadtxt(datafile)
points = np.insert(raw_data[:,:-1], 0, 1, axis=1)
m,n = np.shape(points)[0], np.shape(points)[1]
values = np.zeros((m, 3))

for i in xrange(m):
    values[i, int(raw_data[i, -1] + 1)] = 1

theta_one = np.random.rand(10, 11)
theta_two = np.random.rand(3, 11)


def cost_function(X, Y, t_one, t_two):
    Y_hat = expit(np.dot(np.insert(expit(np.dot(X, t_one.T)), 0, 1, axis=1), t_two.T)) # sigmoid(Theta2 * (sigmoid(Theta1 * X)))
    return np.sum(np.multiply(-Y, np.log(Y_hat)) - np.multiply(np.subtract(1.0, Y), np.log(Y_hat))) / m


def performance_measure(X, Y, t_one, t_two):
    Y_hat = expit(np.dot(np.insert(expit(np.dot(X, t_one.T)), 0, 1, axis=1), t_two.T)) # sigmoid(Theta2 * (sigmoid(Theta1 * X)))
    J = 0
    for t in xrange(m):
        sys.stdout.write("\r Performance Measure Progress:" + str(t / 5655) + "%")
        sys.stdout.flush()
        sample = np.zeros(3)
        sample[np.argmax(Y_hat[t, :])] = 1
        if not np.array_equal(sample, Y[t, :]):
            J += 1
            if np.array_equal(np.array([1.0, 0.0, 0.0]), Y[t, :]):
                J+=3
    print
    return J


@jit(nopython=True)
def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


@jit(nopython=True)
def sigmoid_gradient(x):
    return np.multiply(expit(x), np.subtract(1, expit(x)))


def backprop(X, Y, t_one, t_two):
    t_one_grad = np.zeros((10, 11))
    t_two_grad = np.zeros((3, 11))

    for t in range(m):
        # sys.stdout.write("\r Backprop Progress:" + str(t / 5655) + "%")
        # sys.stdout.flush()
        aone = X[t, :]
        ztwo = np.dot(aone, t_one.T)
        atwo = np.insert(expit(ztwo), 0, 1)
        zthree = np.dot(atwo, t_two.T)
        y_hat = expit(zthree)
        y = Y[t, :]

        deltathree = np.subtract(y_hat, y)
        deltatwo = np.dot(deltathree, np.multiply(t_two, sigmoid_gradient(np.insert(ztwo, 0, 1))))

        t_one_grad = np.add(t_one_grad, np.dot(np.array([deltatwo[1:]]).T, np.array([aone])))
        t_two_grad += np.dot(np.array([deltathree]).T, np.array([atwo]))
    t_one_grad /= m
    t_two_grad /= m

    print
    return t_one_grad, t_two_grad


def backprop_wrapper(theta):
    t_one = np.reshape(theta[:110], (10, 11))
    t_two = np.reshape(theta[110:], (3, 11))
    t_one_grad, t_two_grad = backprop(points, values, t_one, t_two)
    return np.hstack((t_one_grad.ravel(), t_two_grad.ravel()))


def cost_function_wrapper(theta):
    t_one = np.reshape(theta[:110], (10, 11))
    t_two = np.reshape(theta[110:], (3, 11))
    J = cost_function(points, values, t_one, t_two)
    perf = performance_measure(points, values, t_one, t_two)
    print " Iteration " + str(backprop_iter) + " cost: " + str(J) + ", performance: " + str(perf) + "/565545 correct (" + str(int(perf * 100 / float(m))) + "%)"
    return J


def performance_measure_wrapper(theta):
    t_one = np.reshape(theta[:110], (10, 11))
    t_two = np.reshape(theta[110:], (3, 11))
    perf = performance_measure(points, values, t_one, t_two)
    print " Iteration " + str(backprop_iter) + "performance: " + str(perf) + "/565545 correct (" + str(int(perf * 100 / float(m))) + "%)"
    return perf





# trained_weights = open('weights/trained_weights_test_2.txt', 'w')
# weights = fmin_cg(cost_function_wrapper, np.hstack((theta_one.ravel(), theta_two.ravel())), fprime=backprop_wrapper, epsilon=0.001, maxiter=5)
# print weights
# np.savetxt(trained_weights, weights)
#
# print performance_measure(points, values, np.reshape(weights[:110], (10, 11)), np.reshape(weights[110:], (3, 11)))
# trained_weights.close()
