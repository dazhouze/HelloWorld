#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

class AdalineGD(object):
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
	'''
	def __init__(self, eta=0.01, n_iter=50):
		self.__eta = eta
		self.__n_iter = n_iter

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
			output = self.net_input(X)
			errors = (y - output)
			self.__w[1:] += self.__eta * X.T.dot(errors)  # weight
			self.__w[0] += self.__eta * errors.sum()  # bias
			cost = (errors ** 2).sum()/2
			self.__cost.append(cost)
		return self

	def get_cost(self):
		return self.__cost

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

	# view epochs for 2 diff learning rate
	fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
	ada1 = AdalineGD(eta=0.01, n_iter=10).fit(X,y)
	ax[0].plot(range(1, len(ada1.get_cost()) + 1), np.log10(ada1.get_cost()), marker = 'o', color='blue')
	ax[0].set_xlabel('Epochs')
	ax[0].set_ylabel('log(Sum-squared-error)')
	ax[0].set_title('Adaline - Learning rate 0.01')
	ada2 = AdalineGD(eta=0.0001, n_iter=10).fit(X, y)
	ax[1].plot(range(1, len(ada2.get_cost()) +1), ada2.get_cost(), marker='o', color='blue')
	ax[1].set_xlabel('Epochs')
	ax[1].set_ylabel('Sum-squared-error')
	ax[1].set_title('Adaline - Learning rate 0.0001')
	fig.savefig('Iris_learning_rate.pdf')

	# stantardization: make prev distribution to standard normal distribution.
	X_std = np.copy(X)
	X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
	X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

	ada = AdalineGD(n_iter=15, eta=0.01)
	ada.fit(X_std, y)

	from matplotlib.backends.backend_pdf import PdfPages
	with PdfPages('Iris_standard.pdf') as pdf_out:
		fig = plt.figure()
		plot_decision_regions(X_std, y, classifier=ada)
		plt.title('Adaline - Gradient Descent')
		plt.xlabel('sepal length [standardized]')
		plt.ylabel('pepal length [standardized]')
		plt.legend(loc='upper left')
		pdf_out.savefig(fig)
	
		fig = plt.figure()
		plt.plot(range(1, len(ada.get_cost())+1), ada.get_cost(), marker='o', color='blue')
		plt.xlabel('Epochs')
		plt.ylabel('Sum-squared-error')
		pdf_out.savefig(fig)
