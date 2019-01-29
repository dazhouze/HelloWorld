#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

def gini(p):  # Gini impurity
	return (p)*(1-(p)) + (1-p)*(1-(1-p))
def entropy(p):  # entropy
	return - p*np.log2(p) - (1-p)*np.log2((1-p))
def error(p):  # classification error
	return 1-np.max([p, 1-p])
if __name__ == '__main__':

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# plot the impurity indices for the probability range [0, 1] for class 1
		x = np.arange(0, 1, 0.01)
		ent = [entropy(p) if p != 0 else None for p in x]
		sc_ent = [e*0.5 if e else None for e in ent]
		err = [error(i) for i in x]
		fig = plt.figure()
		ax = plt.subplot(111)
		for i, lab, ls, c in zip([ent, sc_ent, gini(x), err], ['Entropy', 'Entropy(scaled)', 'Gini Impurity', 'Misclassification Error'], ['-','-', '--', '-.'], ['black', 'lightgray', 'red', 'green', 'cyan']):
			line = ax.plot(x, i, label=lab, linestyle=ls, lw=2, color=c)
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=5, fancybox=True, shadow=False)
		ax.axhline(y=0.5, linewidth=1, color='k', linestyle='--')
		ax.axhline(y=1.0, linewidth=1, color='k', linestyle='--')
		plt.ylim([0, 1.1])
		plt.xlabel('p(i=1)')
		plt.ylabel('Impurity Index')
		fig.savefig('decision_tree.pdf')
		
		# prepare data
		from ML_03_1_sklearn_perceptron import prepare_data
		X_train_std, X_test_std, y_train, y_test = prepare_data()
		
		X_combined_std = np.vstack((X_train_std, X_test_std))
		y_combined = np.hstack((y_train, y_test))
		
		# deicision tree
		from sklearn.tree import DecisionTreeClassifier
		from ML_03_1_sklearn_perceptron import plot_decision_regions 
		for max_depth in range(1, 7):
			tree = DecisionTreeClassifier(criterion='gini', max_depth=max_depth, random_state=1)
			tree.fit(X_train_std, y_train)

			fig = plt.figure()
			plot_decision_regions(X_combined_std, y_combined, classifier=tree, test_idx=range(105, 150))
			plt.xlabel('pental length [cm]')
			plt.ylabel('pental width [cm]')
			plt.legend(loc='upper left')
			plt.title('Decision Tree depth=%d' % max_depth)
			pdf_all.savefig()
		
		# Random Forest
		from sklearn.ensemble import RandomForestClassifier
		# n_estimators: The number of trees in the forest.
		# n_jobs: The number of jobs to run in parallel for both fit and predict
		forest = RandomForestClassifier(criterion='gini', n_estimators=25, random_state=1, n_jobs=4)
		forest.fit(X_train_std, y_train)
		fig = plt.figure()
		plot_decision_regions(X_combined_std, y_combined, classifier=forest, test_idx=range(105, 150))
		plt.xlabel('pental length')
		plt.ylabel('pental width')
		plt.legend(loc='upper left')
		plt.title('Random Forest')
		pdf_all.savefig()
