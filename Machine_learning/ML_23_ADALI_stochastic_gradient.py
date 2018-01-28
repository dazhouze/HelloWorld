#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import seed as seed

class AdalineSGD(object):
	'''ADAptive LInear NEuron classifier.
	Parameters
	----------
	__eta: float
		Learning rate (between 0.0 and 1.0)
	__n_iter: int
		Passes over the training dataset.
	Attributes
	----------
	__W: 1d-array
		Weights after fitting.
	__errors: list
		Number of misclassifications in every epoch.
	__shuffle: bool (default: True)
		shuffles traning data every epoch.
		if True to prevent cycles.
	__random_state: int (default: None)
		Set random state for fhuffling and initializing the weights.
	'''
	def __init__(self, eta=0.01, n_iter=10, shuffle=True, random_state=None):
		self.__eta = eta
		self.__n_iter = n_iter
		self.__w_initialized = False
		self.__shuffle = shuffle
		if random_state:
			seed(random_state)

	def fit(self, X, y):
		'''Fit training data.
		Parameters
		----------
		X: {array-like}, shape = [n_samples, n_features]
			Training vectors, where n_samples is the number 
			of samples and n_feature is the number of features.
		y: array-linke, shape = [n_samples]
			Target values.
		Returns
		-------
		self: object
		'''
		self.__w = np.zeros(1 + X.shape[1])
		self.__cost = []
		for i in range(0, self.__n_iter):
			if self.__shuffle:
				X, y = self.__shuffle_it(X, y)
			cost = []
			for xi, target in zip(X, y):
				cost.append(self.__update_weights(xi, target))
			avg_cost = sum(cost)/len(y)  # average cost
			self.__cost.append(avg_cost)
		return self

	def get_cost(self):
		return self.__cost

	def partial_fit(self, X, y):
		'''Fit training data without reinitializing the weigths.'''
		if not self.__w_initialzed:
			self.__initialize_weigths(X.shape[1])
		if y.ravel().shape[0] > 1:
			for xi, target in zip (X, y):
				self.__update_weights(xi, target)
		else:
			self.__update_weights(X, y)
		return self

	def __shuffle_it(self, X, y):
		'''Shuffle training data.'''
		r = np.random.permutation(len(y))
		return X[r], y[r]

	def __initialize_weights(self, m):
		'''Initialize weights to zeros.'''
		self.__w = np.zeros(1+m)
		self.__w_initialized = True

	def __update_weights(self, xi, target):
		'''Apply Adaline learning rule to update the weights.'''
		output = self.net_input(xi)
		error = (target - output)
		self.__w[1:] += self.__eta * xi.dot(error)
		self.__w[0] ++ self.__eta * error
		cost = 0.5 * error**2
		return cost

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self.__w[1:]) + self.__w[0]

	def activation(self, X):
		'''Compute linear activation.'''
		return self.net_input(X)

	def predict(self, X):
		'''Return class label after unit step.'''
		return np.where(self.activation(X) >= 0, 1, -1)

if __name__ == '__main__':
	from ML_21_Perceptron import plot_decision_regions as plot_decision_regions
	# prepare data
	df = pd.read_csv('iris.data', header=None)
	y = df.iloc[0:100, 4].values
	y = np.where( y == 'Iris-setosa', -1, 1)  # convert labels into two integer class labels 1, -1
	X = df.iloc[0:100, [0, 2]].values # training vectors

	# stantardization: make prev distribution to standard normal distribution.
	X_std = np.copy(X)
	X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
	X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()
	ada = AdalineSGD(n_iter=15, eta=0.01, random_state=1)
	ada.fit(X_std, y)

	from matplotlib.backends.backend_pdf import PdfPages
	with PdfPages('Iris_StochasticGD.pdf') as pdf_out:
		fig = plt.figure()
		plot_decision_regions(X_std, y, classifier=ada)
		plt.title('Adaline - Stochastic Gradient Descent')
		plt.xlabel('sepal length [standardized]')
		plt.ylabel('pepal length [standardized]')
		plt.legend(loc='upper left')
		pdf_out.savefig(fig)
	
		fig = plt.figure()
		plt.plot(range(1, len(ada.get_cost())+1), ada.get_cost(), marker='o', color='blue')
		plt.xlabel('Epochs')
		plt.ylabel('Average Cost')
		pdf_out.savefig(fig)
