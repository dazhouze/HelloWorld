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
	print(y,np.shape(X), np.shape(y))
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

	from sklearn.svm import SVC
	svm = SVC(kernel='linear', C=1, random_state=1)
	svm.fit(X_train_std, y_train)

	fig = plt.figure()
	from ML_31_scikitlearn_perceptron import plot_decision_regions
	plot_decision_regions(X_combined_std, y_combined, classifier=svm, test_idx=range(105,150))
	plt.xlabel('petal length [standardized]')
	plt.ylabel('petal width [standardized]')
	plt.legend(loc='upper left')
	fig.savefig('svm.pdf')
	
	fig = plt.figure()
	np.random.seed(1)
	X_xor = np.random.randn(200, 2)
	y_xor = np.logical_xor(X_xor[:, 0] > 0, X_xor[:, 1] > 0)
	y_xor = np.where(y_xor, 1, -1)
	plt.scatter(X_xor[y_xor == 1, 0], X_xor[y_xor == 1, 1], c='b', marker='x', label='-1')
	plt.scatter(X_xor[y_xor == -1, 0], X_xor[y_xor == -1, 1], c='r', marker='s', label='-1')
	plt.xlim([-3, 3])
	plt.ylim([-3, 3])
	plt.legend(loc='best')
	fig.savefig('xor.pdf')

	# RBF: Radial Basis Function / Gaussian kernel
	svm = SVC(kernel='rbf', random_state=1, gamma=0.1, C=10)
	svm.fit(X_xor, y_xor)
	fig = plt.figure()
	plot_decision_regions(X_xor, y_xor, classifier=svm)
	plt.legend(loc='upper left')
	fig.savefig('gaussian_kernel.pdf')
	
	svm = SVC(kernel='rbf', random_state=1, gamma=0.2, C=1)
	svm.fit(X_train_std, y_train)
	fig = plt.figure()
	plot_decision_regions(X_combined_std, y_combined, classifier=svm, test_idx=range(105,150))
	plt.xlabel('petal length [standardized]')
	plt.ylabel('petal width [standardized]')
	plt.legend(loc='upper left')
	fig.savefig('gaussian_iris_gamma002.pdf')

	svm = SVC(kernel='rbf', random_state=1, gamma=100, C=1)
	svm.fit(X_train_std, y_train)
	fig = plt.figure()
	plot_decision_regions(X_combined_std, y_combined, classifier=svm, test_idx=range(105,150))
	plt.xlabel('petal length [standardized]')
	plt.ylabel('petal width [standardized]')
	plt.legend(loc='upper left')
	fig.savefig('gaussian_iris_gamma100.pdf')
