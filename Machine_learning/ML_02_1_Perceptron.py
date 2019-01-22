#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import pandas as pd
import os.path

class Perceptron(object):
	'''Rerceptron classifier.
	Parameters
	----------
	eta(η): float
		Learing rate (between 0.0 and 1.0)
	n_iter(epoch): int
		Passes over the traing dataset.

	Attributes
	----------
	_w : 1d-array
		Weights after fitting.
	errors: list
		Number of misclassifiation in every epoch.
	'''
	def __init__(self, eta=0.01, n_iter=10, random_state=1):
		self.eta = eta  # η learning rate
		self.n_iter = n_iter  # epoch, nuber of passes over
		self.random_state = random_state  # seed

	def fit(self, X, y):
		'''Fit training data.
		Parameters
		----------
		X: 2D array. shape = [n_samples, n_features]
			Training vectors, where n_samples is the number
			of samples and n_feature is the number of features.
		y: list. shape = [n_samples]
			Target values.

		Returns
		-------
		self: object
		'''
		rgen = np.random.RandomState(self.random_state)  # set seed
		self._w = rgen.normal(loc=0, scale=0.01, size=1+X.shape[1])  # wTx
		self.errors = []  # log of errors

		for i in range(0, self.n_iter):
			errors = 0
			for xi, target in zip(X, y):
				update = self.eta * (target - self.predict(xi))
				self._w[1:] += update * xi  # ∆wj =η(y(i)−yˆ(i))x(i)
				self._w[0] += update  # bias, -θ, ∆w0 =η(y(i) −output(i))
				errors += int(update != 0.0)
			self.errors.append(errors)
		return self

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self._w[1:]) + self._w[0]

	def predict(self, X):
		'''Return class label after unit step.'''
		return np.where(self.net_input(X) >= 0.0, 1, -1)

	def errors(self):
		return self.errors

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
		plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1],\
				alpha=0.8, c=cmap(idx),\
				marker=markers[idx], label=cl)

def prepare_data(path):
	df = pd.read_csv(path, header=None)
	print(df.tail())
	y = df.iloc[:100, 4].values  # first 100 rows' type
	y = np.where(y == 'Iris-setosa', -1, 1)  # convert labels into two integer class labels 1, -1
	X = df.iloc[:100, [0, 2]].values # training vectors, first 100 rows, 2 features
	return X, y

if __name__ == '__main__':
	# prepare data
	X, y = prepare_data('./data/iris.data')

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# view data
		fig = plt.figure()
		plt.scatter(X[0:50, 0], X[0:50, 1], color='red', marker = 'o', label = 'setosa')
		plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker = 'x', label = 'versicolor')
		plt.xlabel('sepal lenght')
		plt.ylabel('pepal lenght')
		plt.legend(loc='upper left')
		pdf_all.savefig()
		
		# perceptron errors
		ppn = Perceptron(eta=0.1, n_iter = 10)
		ppn.fit(X, y)  # X is traing vectors, y is converted labels
		fig = plt.figure()
		plt.plot(range(1, len(ppn.errors) + 1), ppn.errors, marker='o', color='blue')
		plt.xlabel('Epoces')
		plt.ylabel('Number of misclassifications')
		pdf_all.savefig()
		
		# decision boundary
		fig = plt.figure()
		plot_decision_regions(X, y, classifier=ppn)
		plt.xlabel('sepal length (cm)')
		plt.ylabel('pepal length (cm)')
		plt.legend(loc='upper left')
		pdf_all.savefig()
