#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

class AdalineGD(object):
	'''ADAptive LInear NEuron classifier.
	Parameters
	----------
	_eta(η): float
		Learning rate (between 0.0 and 1.0)
	_n_iter(epoch): int
		Passes over the training dataset.
	random_state: int
		Random number generator seed for wight init.
	Attributes
	----------
	_w: 1d-array
		Weights after fitting.
	cost: list
		Sum of squares cost func in every epoch.
	'''
	def __init__(self, eta=0.01, n_iter=50, random_state=1):
		self._eta = eta
		self._n_iter = n_iter
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
		rgen = np.random.RandomState(self.random_state)  # set seed
		self._w = rgen.normal(loc=0, scale=0.01, size=1+X.shape[1])
		self.cost = []  # log of cost
		for i in range(0, self._n_iter):
			net_input = self.net_input(X)
			output = self.activation(net_input)  # activation func
			errors = (y - output)
			self._w[1:] += self._eta * X.T.dot(errors)  # weight
			self._w[0] += self._eta * errors.sum()  # bias
			cost = (errors**2).sum() / 2
			self.cost.append(cost)
		return self

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

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# view epochs for 2 diff learning rate
		fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
		ada1 = AdalineGD(eta=0.01, n_iter=10).fit(X,y)
		ax[0].plot(range(1, len(ada1.cost) + 1), np.log10(ada1.cost), marker = 'o', color='blue')
		ax[0].set_xlabel('Epochs')
		ax[0].set_ylabel('log(Sum-squared-error)')
		ax[0].set_title('Adaline - Learning rate 0.01')
		ada2 = AdalineGD(eta=0.0001, n_iter=10).fit(X, y)
		ax[1].plot(range(1, len(ada2.cost) +1), ada2.cost, marker='o', color='blue')
		ax[1].set_xlabel('Epochs')
		ax[1].set_ylabel('Sum-squared-error')
		ax[1].set_title('Adaline - Learning rate 0.0001')
		pdf_all.savefig()
		
		# fit
		ada = AdalineGD(n_iter=15, eta=0.01)
		ada.fit(X_std, y)

		fig = plt.figure()
		ML_02_1_Perceptron.plot_decision_regions(X_std, y, classifier=ada)
		plt.title('Adaline - Gradient Descent')
		plt.xlabel('sepal length [standardized]')
		plt.ylabel('pepal length [standardized]')
		plt.legend(loc='upper left')
		pdf_all.savefig()
	
		fig = plt.figure()
		plt.plot(range(1, len(ada.cost)+1), ada.cost, marker='o', color='blue')
		plt.xlabel('Epochs')
		plt.ylabel('Sum-squared-error')
		pdf_all.savefig()
