#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

def plot_decision_regions(X, y, classifier, test_idx = None, resolution=0.02):
	from matplotlib.colors import ListedColormap
	#setup marker generator and color map
	markers = ('s', 'x', 'o', '^', 'v')
	colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
	cmap = ListedColormap(colors[:len(np.unique(y))])

	# plot the decision surface
	x1_min, x1_max = X[:, 0].min()-1, X[:, 0].max()+1
	x2_min, x2_max = X[:, 1].min()-1, X[:, 1].max()+1
	xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
	Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
	Z = Z.reshape(xx1.shape)
	plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
	plt.xlim(xx1.min(), xx1.max())
	plt.ylim(xx2.min(), xx2.max())

	for idx, cl in enumerate(np.unique(y)):
		plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], alpha=0.8, c=colors[idx], marker=markers[idx], label=cl, edgecolor='black')

	# highlight test samples
	if test_idx:
		#plot all samples
		X_test, y_test = X[test_idx, :], y[test_idx]
		plt.scatter(X_test[:,0], X_test[:,1], c='', edgecolor='black', alpha=1.0, linewidth=1, marker='o', s=100, label='test set')

def prepare_data():
    # prepare data
    from sklearn import datasets
    iris = datasets.load_iris()
    X = iris.data[:, [2, 3]]
    y = iris.target
    print('Class labels:', np.unique(y))
    print(X.shape, y.shape)
    
    # split train and test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
    print(X_train.shape, X_test.shape)
    
    print('Labels counts in y:', np.bincount(y))
    print('Labels counts in y_train:', np.bincount(y_train))
    print('Labels counts in y_test:', np.bincount(y_test))
    
    # scaler
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    sc.fit(X_train)  # mean + sd of train data
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)
    return X_train_std, X_test_std, y_train, y_test

if __name__ == '__main__':
	X_train_std, X_test_std, y_train, y_test = prepare_data()

	import  ML_02_1_Perceptron
	ppn = ML_02_1_Perceptron.Perceptron(eta=0.1, n_iter=40, random_state=1)
	ppn.fit(X_train_std, y_train)
	y_pred = ppn.predict(X_test_std)
	print('Chapter 2 perceptron misclassified samples: %d' % (y_test != y_pred).sum())

	# sklearn perceptron
	from sklearn.linear_model import Perceptron
	ppn = Perceptron(eta0=0.1, max_iter=40, random_state=1)
	ppn.fit(X_train_std, y_train)
	y_pred = ppn.predict(X_test_std)
	print('sklearn perceptron misclassified samples: %d' % (y_test != y_pred).sum())
	
	# accuracy
	from sklearn.metrics import accuracy_score
	print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))

	X_combined_std = np.vstack((X_train_std, X_test_std))
	y_combined = np.hstack((y_train, y_test))
	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure()
		plot_decision_regions(X=X_combined_std, y=y_combined, classifier=ppn, test_idx=range(105,150))
		plt.xlabel('petal length [standardized')
		plt.ylabel('petal width [standardized')
		plt.legend(loc='upper left')
		pdf_all.savefig()
