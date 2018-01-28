#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def sigmoid(z):
	return 1/(1 + np.exp(-z))
class LogisticRegressionGD(object):
	'''Logistic Regression Classifier using gradient descent.
	Parameters
	----------
	__eta: float
		Learnging rate (between 0.0 and 1.0)
	__n_iter: int
		Passes over the training dataset.
	__random_state: int
		Random number generator seed for random weight initialization.
	Attributies
	-----------
	__w: 1d-array
		Weights after fitting.
	__cost: list
		Sum-of-squares cost funciton value in each epoch.
	'''
	def __init__(self, eta=0.05, n_iter=100, random_state=1):
		self.__eta = eta
		self.__n_iter = n_iter
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
		self.__w = rgen.normal(loc=0, scale=0.01, size=1+X.shape[1])
		self.__cost = []

		for i in range(self.__n_iter):
			net_input = self.net_input(X)
			output= self.activation(net_input)
			errors = (y - output)
			self.__w[1:] += self.__eta*X.T.dot(errors)
			self.__w[0] += self.__eta*errors.sum()


			'''note that we compute the logistic 'cost' now
			instead of the sum of squared errors cost
			'''
			cost = (-y.dot(np.log(output)) - ((1-y).dot(np.log(1-output))))
			self.__cost.append(cost)
		return self

	def net_input(self, X):
		'''Calculate net input.'''
		return np.dot(X, self.__w[1:]) + self.__w[0]

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
	z = np.arange(-7, 7, 0.1)
	phi_z = sigmoid(z)
	fig = plt.figure()
	plt.plot(z, phi_z)
	plt.axvline(0, color='k')
	plt.ylim(-0.1, 1.1)
	plt.xlabel('z')
	plt.ylabel('$\phi (z)$')
	plt.yticks([0.0, 0.5, 1])
	ax = plt.gca()
	ax.yaxis.grid(True)
	fig.savefig('sigmoid.pdf')
	
	# cost of classifying a single-sample instance for different values of phi(z)
	fig = plt.figure()
	def cost_1(z):
		return - np.log(sigmoid(z))
	def cost_0(z):
		return - np.log(1-sigmoid(z))
	z = np.arange(-10, 10, 0.1)
	phi_z = sigmoid(z)
	c1 = [cost_1(x) for x in z]
	plt.plot(phi_z, c1, label='J(w) if y =1')
	c0 = [cost_0(x) for x in z]
	plt.plot(phi_z, c0, linestyle='--', label='J(w) if y =0')
	plt.ylim(0, 5.1)
	plt.xlim([0, 1])
	plt.xlabel('$\phi$(z)')
	plt.ylabel('J(w)')
	plt.legend(loc='best')
	fig.savefig('sigmoid_cost.pdf')
	
	# sigmoid
	# prepare data
	from sklearn import datasets
	iris = datasets.load_iris()
	X = iris.data[:, [2, 3]]
	y = iris.target
	print('Class labels:', np.unique(y))
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

	#from sklearn.preprocessing import StandardScaler
	#sc = StandardScaler()
	#sc.fit(X_train)
	#X_train_std = sc.transform(X_train)
	#X_test_std = sc.transform(X_test)

	X_train_01_subset = X_train[(y_train == 0) | (y_train == 1)] 
	y_train_01_subset = y_train[(y_train == 0) | (y_train == 1)] 
	lrgd = LogisticRegressionGD(eta=0.05, n_iter=1000, random_state=1)
	lrgd.fit(X_train_01_subset, y_train_01_subset)

	from ML_31_scikitlearn_perceptron import plot_decision_regions as plot_decision_regions
	fig = plt.figure()
	plot_decision_regions(X=X_train_01_subset, y=y_train_01_subset, classifier=lrgd)
	plt.xlabel('petal length [stardardized]')
	plt.ylabel('pental width [standardized]')
	plt.legend(loc='upper left')
	fig.savefig('sigmoid_devision_region.pdf')
