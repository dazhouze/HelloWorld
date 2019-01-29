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

		# KNN
		from sklearn.neighbors import KNeighborsClassifier
		knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
		knn.fit(X_train_std, y_train)
		fig = plt.figure()
		from ML_03_1_sklearn_perceptron import plot_decision_regions
		plot_decision_regions(X_combined_std, y_combined, classifier=knn, test_idx=range(105, 150))
		plt.xlabel('petal length [stanardized]')
		plt.ylabel('petal width [stanardized]')
		plt.legend(loc='upper left')
		pdf_all.savefig()
