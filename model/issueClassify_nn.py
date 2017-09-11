import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.preprocessing import OneHotEncoder
data = loadmat('data/ex3data1.mat')

X = data['X']
y = data['y']

encorder = OneHotEncoder(sparse=False)
y_onehot = encorder.fit_transform(y)

def sigmod(z):
	return 1 / (1+np.exp(-z))

def forward_propagate(X, theta1, theta2):
	m = X.shape[0]

	a1 = np.insert(X, 0, values=np.ones(m), axis=1)
	z2 = a1 * theta1.T
	a2 = np.insert(sigmod(z2), 0, values=np.ones(m), axis=1)
	z3 = a2 * theta2.T
	h = sigmod(z3)

	return a1, z2, a2, z3, h

def sigmoid_gradient(z):
	return np.multiply(sigmod(z), (1-sigmod(z)))

def cost(params, input_size, hidden_size, num_labels, X, y, learning_rate):
	m = X.shape[0]
	X = np.matrix(X)
	y = np.matrix(y)

	theta1 = np.matrix(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size+1))))
	theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):],(num_labels,(hidden_size + 1))))

	a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

	J = 0
	delta1 = np.zeros(theta1.shape)
	delta2 = np.zeros(theta2.shape)

	for i in range(m):
		first_term = np.multiply(-y[i, :], np.log(h[i, :]))
		second_term = np.multiply((1-y[i,:]), np.log(1-h[i,:]))
		J += np.sum(first_term - second_term)

	J = J/m

	J += (float(learning_rate) / (2*m)) *(np.sum(np.power(theta1[:,1:], 2)))

	for t in range(m):
		a1t = a1[t,:]
		z2t = z2[t,:]
		a2t = a2[t,:]
		ht = h[t,:]
		yt = y[t,:]

		d3t = ht - yt
		z2t = np.insert(z2t, 0, values=np.ones(1))
		d2t = np.multiply((theta2.T * d3t.T).T)
