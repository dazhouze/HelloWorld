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
		
		from sklearn.linear_model import LogisticRegression
		lr = LogisticRegression(C=100, random_state=1)
		lr.fit(X_train_std, y_train)
		
		X_combined_std = np.vstack((X_train_std, X_test_std))
		y_combined = np.hstack((y_train, y_test))
		
		from ML_03_1_sklearn_perceptron import plot_decision_regions
		fig = plt.figure()
		plot_decision_regions(X_combined_std, y_combined, classifier=lr, test_idx=range(105, 150))
		plt.xlabel('petal length [stardardized]')
		plt.ylabel('pental width [standardized]')
		plt.legend(loc='upper left')
		plt.title('Logistic Regression')
		pdf_all.savefig()
		
		# One way of finding a good bias-variance tradeoff is to tune the complexity of
		# the model via regularization. 
		# L2-regularization for aviod overfitting
		weights, params = [], []
		for c in np.arange(-5, 5):
			lr = LogisticRegression(C=10.**c, random_state=1) # C is λ inverse, regularization parameter λ
			lr.fit(X_train_std, y_train)
			weights.append(lr.coef_[1])
			params.append(10.**c)
		weights = np.array(weights)
		fig = plt.figure()
		plt.plot(params, weights[:, 0], label='petal length')
		plt.plot(params, weights[:, 1], label='petal width')
		plt.ylabel('weight coefficient')
		plt.xlabel('C')
		plt.legend(loc='upper left')
		plt.xscale('log')
		plt.title('L2 regularization')
		pdf_all.savefig()

