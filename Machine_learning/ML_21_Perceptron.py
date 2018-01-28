#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


class Perceptron(object):

	'''Rerceptron classifier.

	Parameters
	----------
	__eta: float
		Learing rate (between 0.0 and 1.0)
	__n_iter: int
		Passes over the traing dataset.

	Attributes
	----------
	__w : 1d-array
		Weights after fitting.
	__errors: list
		Number of misclassifiation in every epoch.
	'''

	def __init__(self, eta=0.01, n_iter=10):
		self.__eta = eta
		self.__n_iter = n_iter

	def fit(self, X, y):
		'''Fit training data.

		Parameters
		----------
		X: {array-like}, shape = [n_samples, n_features]
			Training vectors, where n_samples is the number
			of samples and n_feature is the number of features.
		y: array-like, shape = [n_samples]
			Target values.

		Returns
		-------
		self: object
		'''
		self.__w = np.zeros(1 + X.shape[1])  # weigth number is features + 1
		self.__errors = []

		for i in range(0, self.__n_iter):
			error = 0
			for xi, target in zip(X, y):
				update = self.__eta * (target - self.predict(xi))
				self.__w[1:] += update * xi
				self.__w[0] += update
				error += int(update != 0.0)
			self.__errors.append(error)
		return self

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self.__w[1:]) + self.__w[0]

	def predict(self, X):
		'''Return class label after unit step.'''
		return np.where(self.net_input(X) >= 0.0, 1, -1)

	def get_errors(self):
		return self.__errors

def plot_decision_regions(X, y, classifier, resolution=0.02):
	from matplotlib.colors import ListedColormap
	# setup marker generator and color map
	markers = ('s', 'x', 'o', '^', 'v')
	colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
	cmap = ListedColormap(colors[:len(np.unique(y))])  # sorted unique elements of an array
	# plot the decision surface
	x1_min, x1_max = X[:,0].min()-1, X[:,0].max()+1
	x2_min, x2_max = X[:,1].min()-1, X[:,1].max()+1
	xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution)) # paired grid array
	Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
	Z = Z.reshape(xx1.shape)
	plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
	plt.xlim(xx1.min(), xx1.max())
	plt.ylim(xx2.min(), xx2.max())
	# plot class samples
	for idx, cl in enumerate(np.unique(y)):
		plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], alpha=0.8, c=cmap(idx), marker=markers[idx], label=cl)

if __name__ == '__main__':
	# prepare data
	df = pd.read_csv('iris.data', header=None)
	y = df.iloc[0:100, 4].values
	y = np.where( y == 'Iris-setosa', -1, 1)  # convert labels into two integer class labels 1, -1
	X = df.iloc[0:100, [0, 2]].values # training vectors
	# view data
	fig = plt.figure()
	plt.scatter(X[0:50, 0], X[0:50, 1], color='red', marker = 'o', label = 'setosa')
	plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker = 'x', label = 'versicolor')
	plt.xlabel('sepal lenght')
	plt.ylabel('pepal lenght')
	plt.legend(loc='upper left')
	fig.savefig('Iris_ori.pdf')

	# perceptron
	fig = plt.figure()
	ppn = Perceptron(eta=0.1, n_iter = 10)
	ppn.fit(X, y)  # X is traing vectors, y is converted labels
	plt.plot(range(1, len(ppn.get_errors()) + 1), ppn.get_errors(), marker='o', color='blue')
	plt.xlabel('Epoces')
	plt.ylabel('Number of misclassifications')
	fig.savefig('Iris_ppn.pdf')

	# decision boundary
	fig = plt.figure()
	plot_decision_regions(X, y, classifier=ppn)
	plt.xlabel('sepal length (cm)')
	plt.ylabel('pepal length (cm)')
	plt.legend(loc='upper left')
	fig.savefig('Iris_boundary.pdf')
