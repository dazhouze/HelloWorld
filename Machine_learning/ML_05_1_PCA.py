#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
	df_wine = pd.read_csv('./wine.data', header=None)
	from sklearn.model_selection import train_test_split
	X, y = df_wine.iloc[:, 1:].values, df_wine.iloc[:, 0].values
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

	# standardize the features
	from sklearn.preprocessing import StandardScaler
	sc = StandardScaler()
	X_train_std = sc.fit_transform(X_train)
	X_test_std = sc.transform(X_test)

	# obtain the eigenpairs of covariance matrix
	cov_mat = np.cov(X_train_std.T)
	eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)
	#print('\nEigenvalues \n%s' % eigen_vals)
	#print(eigen_vecs)

	# variance explained ratios
	tot = sum(eigen_vals)
	var_exp = [(i/tot) for i in sorted(eigen_vals, reverse=True)]
	cum_var_exp = np.cumsum(var_exp)
	fig = plt.figure()
	plt.bar(range(1, 14), var_exp, alpha=0.5, align='center', label='individual explained variance', color='blue')
	plt.step(range(1, 14), cum_var_exp, where='mid', label='cumulative explained variance', color='blue')
	plt.ylabel('Explained variance ratio')
	plt.xlabel('Principal component index')
	plt.legend(loc='best')
	fig.savefig('variance_explained_ratios.pdf')

	# make a list of (eigenvalue, eigenvector) tuples
	eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:, i]) for i in range(len(eigen_vals))]
	# sort the eigenvalues, eigenvector tuples from high to low
	eigen_pairs.sort(key=lambda k: k[0], reverse=True)

	w = np.hstack((eigen_pairs[0][1][:, np.newaxis], eigen_pairs[1][1][:, np.newaxis]))
	print('Matrix W:\n', w)

	X_train_pca = X_train_std.dot(w)
	
	# visualization
	colors = ['r', 'b', 'g']
	markers = ['s', 'x', 'o']
	fig = plt.figure()
	for l,c,m in zip(np.unique(y_train), colors, markers):
		plt.scatter(X_train_pca[y_train==l, 0], X_train_pca[y_train==l, 1], c=c, label=l, marker=m)
	plt.xlabel('PC 1')
	plt.ylabel('PC 2')
	plt.legend(loc='lower left')
	fig.savefig('PCA.pdf')


	# PCA in scikit-learn
	from sklearn.linear_model import LogisticRegression
	from sklearn.decomposition import PCA
	pca = PCA(n_components=2)
	lr = LogisticRegression()
	X_train_pca = pca.fit_transform(X_train_std)
	X_test_pca = pca.transform(X_test_std)
	lr.fit(X_train_pca, y_train)
	fig = plt.figure()
	from ML_31_scikitlearn_perceptron import plot_decision_regions
	plot_decision_regions(X_train_pca, y_train, classifier=lr)
	plt.xlabel('PC 1')
	plt.ylabel('PC 2')
	plt.legend(loc='lower left')
	fig.savefig('PCA_scikit.pdf')

	pca = PCA(n_components=None)
	X_train_pca = pca.fit_transform(X_train_std)
	print('scikit PCA explained varience ratio:\n', pca.explained_variance_ratio_)
