#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
	# prepare data
	from sklearn import datasets
	iris = datasets.load_iris()
	X = iris.data[:, [2, 3]]
	y = iris.target
	print('Class labels:', np.unique(y))
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

	from sklearn.preprocessing import StandardScaler
	sc = StandardScaler()
	sc.fit(X_train)
	X_train_std = sc.transform(X_train)
	X_test_std = sc.transform(X_test)
	X_combined_std = np.vstack((X_train_std, X_test_std))
	y_combined = np.hstack((y_train, y_test))

	from sklearn.linear_model import LogisticRegression
	lr = LogisticRegression(C=100, random_state=1)
	lr.fit(X_train_std, y_train)
	fig = plt.figure()
	from ML_31_scikitlearn_perceptron import plot_decision_regions as plot_decision_regions
	plot_decision_regions(X_combined_std, y_combined, classifier=lr, test_idx=range(105, 150))
	plt.xlabel('petal length [stardardized]')
	plt.ylabel('pental width [standardized]')
	plt.legend(loc='upper left')
	fig.savefig('sigmoid_devision_region.pdf')
	
	# L2-regularization path for the two weight coefficients
	weights, params = [], []
	for c in np.arange(-5, 5):
		lr = LogisticRegression(C=10.0**c, random_state=1)
		lr.fit(X_train_std, y_train)
		weights.append(lr.coef_[1])
		params.append(10.0**c)
	weights = np.array(weights)
	fig = plt.figure()
	plt.plot(params, weights[:, 0], label='petal length')
	plt.plot(params, weights[:, 1], label='petal width')
	plt.ylabel('weight coefficient')
	plt.xlabel('C')
	plt.legend(loc='upper left')
	plt.xscale('log')
	fig.savefig('L2-regularization.pdf')
