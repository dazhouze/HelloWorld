#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

'''
PCA:
1. Standardize the d-dimentisonal dataset.
2. Construct the conariance matrix.
3. Decompose covariance matrix into its eigenvectors and eigenvalues.
4. Sort the eigenvalues by decreasing order to rank the corresponding eigenvectors.
5. Select K eigenvectors which correspond to the K largest eigenvalues,
	where k is the dimensionaltiy of the new features subspace (k<=d).
6. Construct a projection matrix W from the "top" k eigenvectors.
7. Transform the d-dimensional input dataset X using the projection matrix W
	to obtain the new k-dimensional feature subspace.
'''

if __name__ == '__main__':

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:

		df_wine = pd.read_csv('./data/wine.data', header=None)
		X, y = df_wine.iloc[:, 1:].values, df_wine.iloc[:, 0].values
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
		
		# standardize the features
		sc = StandardScaler()
		X_train_std = sc.fit_transform(X_train)
		X_test_std = sc.transform(X_test)
		
		# obtain the eigenpairs of covariance matrix
		cov_mat = np.cov(X_train_std.T)  # np.cov: covariance indication
		eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)  # eigenvectors of the covariance matrix represent the principal components
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
		pdf_all.savefig(fig)

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
