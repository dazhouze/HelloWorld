#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

if __name__ == '__main__':
	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# prepare data
		from ML_03_1_sklearn_perceptron import prepare_data
		X_train_std, X_test_std, y_train, y_test = prepare_data()
		
		X_combined_std = np.vstack((X_train_std, X_test_std))
		y_combined = np.hstack((y_train, y_test))
	
		# SVM, linearly
		from sklearn.svm import SVC
		svm = SVC(kernel='linear', C=1, random_state=1) # C: penalty for misclassification. 
		svm.fit(X_train_std, y_train)

		from ML_03_1_sklearn_perceptron import plot_decision_regions
		fig = plt.figure()
		plot_decision_regions(X_combined_std, y_combined, classifier=svm, test_idx=range(105, 150))
		plt.xlabel('petal length [stardardized]')
		plt.ylabel('pental width [standardized]')
		plt.legend(loc='upper left')
		plt.title('SVM')
		pdf_all.savefig()
		
		# dataset that has the form of an XOR gate
		np.random.seed(1)
		X_xor = np.random.randn(200, 2)
		y_xor = np.logical_xor(X_xor[:,0] > 0,\
				X_xor[:,1] > 0)
		y_xor = np.where(y_xor, 1, -1)
		fig = plt.figure()
		plt.scatter(X_xor[y_xor == 1, 0], X_xor[y_xor == 1, 1], c='b', marker='x', label='1')
		plt.scatter(X_xor[y_xor == -1, 0], X_xor[y_xor == -1, 1], c='r', marker='s', label='-1')
		plt.xlim([-3, 3])
		plt.ylim([-3, 3])
		plt.legend(loc='best')
		plt.title('XOR gate')
		pdf_all.savefig()

		# RBF: Radial Basis Function / Gaussian kernel
		for gamma in (0.1, 0.2, 0.5, 100):  # γ parameter, cut-off parameter for the Gaussian sphere
			svm = SVC(kernel='rbf', random_state=1, gamma=gamma, C=1)
			svm.fit(X_train_std, y_train)
			fig = plt.figure()
			plot_decision_regions(X_combined_std, y_combined, classifier=svm, test_idx=range(105,150))
			plt.xlabel('petal length [standardized]')
			plt.ylabel('petal width [standardized]')
			plt.legend(loc='upper left')
			plt.title('Nonlinear SVM γ=%.1f' % gamma)
			pdf_all.savefig()
