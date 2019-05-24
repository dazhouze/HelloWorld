#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

from sklearn.base import clone
from itertools import combinations
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# SBS
'''
A classic sequential feature selection algorithm is Sequential Backward Selection (SBS), which aims to reduce the dimensionality of the initial feature subspace with a minimum decay in performance of the classifier to improve upon computational efficiency.
'''

class SBS(object):
	def __init__(self, estimator, k_features, scoring=accuracy_score, test_size=0.25, random_state=1):
		self.scoring = scoring
		self.estimator = clone(estimator)
		self.k_features = k_features
		self.test_size = test_size
		self.random_state = random_state

	def fit(self, X, y):
		X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
		dim = X_train.shape[1]
		self._indices = tuple(range(dim))
		self._subsets = [self._indices]
		score = self._calc_score(X_train, y_train, X_test, y_test, self._indices)
		self._scores = [score]

		while dim > self.k_features:
			scores = []
			subsets = []
			
			for p in combinations(sefl._indices, r=dim-1):
				score = self._calc_score(X_train, y_train, X_test, y_test, p)
				scores.append(score)
				subsets.append(p)

			best = np.argmax(scores)
			self._indices = subsets[best]
			self._subsets.append(self._indices)
			dim -= 1

			self._score.append(scores[best])
		self.k_score = self._scores[-1]
	
		return self

	def transform(self, X):
		return X[:, self._indices]

	def _calc_score(self, X_train, y_train, X_test, y_test, indices):
		self.estimator.fit(X_train[:, indices], y_train)
		y_pred = self.estimator.predict(X_test[:,indices])
		score = self.scoring(y_test, y_pred)
		return score

	def get_subsets(self):
		return self._subsets

	def get_scores(self):
		return self._scores

if __name__ == '__main__':
	from ML_04_3_train_test_split import load_data, train_test_spliting
	df = load_data()
	X_train, X_test, y_train, y_test = train_test_spliting(df)

	from ML_04_4_scaling import scaling
	X_train_std, X_test_std = scaling(X_train, X_test)

	from sklearn.neighbors import KNeighborsClassifier
	knn = KNeighborsClassifier(n_neighbors=5)
	sbs = SBS(knn, k_features=1)
	sbs.fit(X_train_std, y_train)
	k_feat = [len(k) for k in sbs.get_subsets()]

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure()
		plt.plot(k_feat, sbs.get_scores(), marker='o')
		plot.ylim([0.7, 1.02])
		plt.ylabel('Accuracy')
		plt.xlabel('Number of k_features')
		pdf_all.savefig()

