#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
	def gini(p):
		return (p)*(1-(p)) + (1-p)*(1-(1-p))
	def entropy(p):
		return - p*np.log2(p) - (1-p)*np.log2((1-p))
	def error(p):
		return 1-np.max([p, 1-p])
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
	from sklearn import datasets
	iris = datasets.load_iris()
	X = iris.data[:, [2, 3]]
	y = iris.target
	print('Class labels:', np.unique(y))
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

	# deicision tree
	from sklearn.tree import DecisionTreeClassifier
	tree = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=1)
	tree.fit(X_train, y_train)
	X_combined = np.vstack((X_train, X_test))
	y_combined = np.hstack((y_train, y_test))

	
	fig = plt.figure()
	from ML_31_scikitlearn_perceptron import plot_decision_regions 
	plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105, 150))
	plt.xlabel('pental length [cm]')
	plt.ylabel('pental width [cm]')
	plt.legend(loc='upper left')
	fig.savefig('decision_tree_iris.pdf')

	from sklearn.ensemble import RandomForestClassifier
	forest = RandomForestClassifier(criterion='gini', n_estimators=25, random_state=1, n_jobs=4)
	forest.fit(X_train, y_train)
	fig = plt.figure()
	plot_decision_regions(X_combined, y_combined, classifier=forest, test_idx=range(105, 150))
	plt.xlabel('pental length')
	plt.ylabel('pental width')
	plt.legend(loc='upper left')
	fig.savefig('random_forest.pdf')
