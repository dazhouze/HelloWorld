#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

class AdalineSGD(object):
	'''ADAptive LInear NEuron classifier.
	Parameters
	----------
	eta: float
		Learning rate (between 0.0 and 1.0)
	n_iter: int
		Passes over the training dataset.
	shuffle: bool (default: True)
		Shuffles trainging data every epoch if True to prevent cycles
	random_state: int
		Random number generator seed for random weight inin
	Attributes
	----------
	_W: 1d-array
		Weights after fitting.
	cost: list
		Sum of squares of cost func value average over all tringing samples in each epoch.
	'''
	def __init__(self, eta=0.01, n_iter=10, shuffle=True, random_state=None):
		self.eta = eta
		self.n_iter = n_iter
		self.w_initialized = False
		self.shuffle = shuffle
		self.random_state = random_state

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
		self.initialize_weights(X.shape[1])
		self.cost = []
		for i in range(0, self.n_iter):
			if self.shuffle:
				X, y = self._shuffle(X, y)
			cost = []
			for xi, target in zip(X, y):
				cost.append(self._update_weights(xi, target))
			self.cost.append(np.mean(cost))  # average cost
		return self

	def partial_fit(self, X, y):
		'''Fit training data without reinitializing the weigths.'''
		if not self._w_initialzed:
			self._initialize_weigths(X.shape[1])
		if y.ravel().shape[0] > 1:
			for xi, target in zip (X, y):
				self._update_weights(xi, target)
		else:
			self._update_weights(X, y)
		return self

	def _shuffle(self, X, y):
		'''Shuffle training data.'''
		r = self._rgen.permutation(len(y))
		return X[r], y[r]

	def initialize_weights(self, m):
		'''Initialize weights to zeros.'''
		self._rgen = np.random.RandomState(self.random_state)
		self._w = self._rgen.normal(loc=0, scale=0.01, size=1+m)
		self._w_initialized = True

	def _update_weights(self, xi, target):
		'''Apply Adaline learning rule to update the weights.'''
		output = self.activation(self.net_input(xi))
		error = (target - output)
		self._w[1:] += self.eta * xi.dot(error)
		self._w[0] ++ self.eta * error
		cost = 0.5 * error**2
		return cost

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self._w[1:]) + self._w[0]

	def activation(self, X):
		'''Compute linear activation.'''
		return X

	def predict(self, X):
		'''Return class label after unit step.'''
		return np.where(self.activation(self.net_input(X)) >= 0, 1, -1)

if __name__ == '__main__':
	import ML_02_1_Perceptron
	# prepare data
	X, y = ML_02_1_Perceptron.prepare_data('./data/iris.data')

	# stantardization: make prev distribution to standard normal distribution.
	X_std = scale(X, axis=0)

	ada = AdalineSGD(n_iter=15, eta=0.01, random_state=1)
	ada.fit(X_std, y)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure()
		ML_02_1_Perceptron.plot_decision_regions(X_std, y, classifier=ada)
		plt.title('Adaline - Stochastic Gradient Descent')
		plt.xlabel('sepal length [standardized]')
		plt.ylabel('pepal length [standardized]')
		plt.legend(loc='upper left')
		pdf_all.savefig()
	
		fig = plt.figure()
		plt.plot(range(1, len(ada.cost)+1), ada.cost, marker='o', color='blue')
		plt.xlabel('Epochs')
		plt.ylabel('Average Cost')
		pdf_all.savefig()
