#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

class LogisticRegressionGD(object):
	'''Logistic Regression Classifier using gradient descent.
	Parameters
	----------
	eta: float
		Learnging rate (between 0.0 and 1.0)
	n_iter: int
		Passes over the training dataset.
	_random_state: int
		Random number generator seed for random weight initialization.
	Attributies
	-----------
	_w: 1d-array
		Weights after fitting.
	cost: list
		Sum-of-squares cost funciton value in each epoch.
	'''
	def __init__(self, eta=0.05, n_iter=100, random_state=1):
		self.eta = eta
		self.n_iter = n_iter
		self.random_state = random_state

	def fit(self, X, y):
		'''Fit training data.
		Parameters
		----------
		X: {array-like}, shap = [n_sample, n_features]
			Training vectors, where n_samples is the number
			of samples and n_features if the number of features.
		y: array-linke, shap = [n_samples]
			TARGET Valuse.
		Returns
		-------
		self: object
		'''
		rgen = np.random.RandomState(self.random_state)
		self._w = rgen.normal(loc=0, scale=0.01, size=1+X.shape[1])
		self.cost = []

		for i in range(self.n_iter):
			net_input = self.net_input(X)
			output= self.activation(net_input)
			errors = (y - output)
			self._w[1:] += self.eta*X.T.dot(errors)
			self._w[0] += self.eta*errors.sum()


			'''note that we compute the logistic 'cost' now
			instead of the sum of squared errors cost
			'''
			cost = (-y.dot(np.log(output)) - ((1-y).dot(np.log(1-output))))
			self.cost.append(cost)
		return self

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self._w[1:]) + self._w[0]

	def activation(self, z):
		'''Compute logistic sigmoid activation.'''
		return 1/(1+np.exp(-np.clip(z, -250,250)))

	def predict(self, X):
		'''Return class label after unit step.'''
		return np.where(self.net_input(X) >= 0, 1, 0)
		'''equivalent to :
		return np.where(self.activation(self.net_input(X)) >= 0.5, 1, 0)
		'''

if __name__ == '__main__':
	# prepare data
	from ML_03_1_scipy_perceptron import prepare_data
        X_train_std, X_test_std, y_train, y_test = prepare_data()

	X_train_01_subset = X_train[(y_train == 0) | (y_train == 1)] 
	y_train_01_subset = y_train[(y_train == 0) | (y_train == 1)] 
	lrgd = LogisticRegressionGD(eta=0.05, n_iter=1000, random_state=1)
	lrgd.fit(X_train_01_subset, y_train_01_subset)

	from ML_03_1_sklearn_perceptron import plot_decision_regions
	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure()
		plot_decision_regions(X=X_train_01_subset, y=y_train_01_subset, classifier=lrgd)
		plt.xlabel('petal length [stardardized]')
		plt.ylabel('pental width [standardized]')
		plt.legend(loc='upper left')
		pdf_all.savefig()
