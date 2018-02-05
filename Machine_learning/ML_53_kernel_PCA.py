#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def rbf_kernel_pca(X, gama, n_components):
	from scipy.spatial.distance import pdist, squareform
	from scipy import exp
	from scipy.linalg import eigh
	'''
	Radial Basis Function / Gaussian kernel
	Parameters
	----------
	X: {NumPy ndarray}, shape, [n_samples, n_features]
	gamma: float
		Turning parameter of the RBF kernel.
	n_components: int
		Number of principal compoents to return.
	Returns
	-------
	X_pc: {NumPy ndarray}, shape = [n_samples, k_featrues]
		Project dataset
	'''
	# Calculate pairwise squared Euclidean distances in the M*N dimensional dataset.
	sq_dists = pdist(X, 'sqeuclidean')
	# Convert parwise distances into a square matrix.
	mat_sq_dists = squareform(sq_dists)
	# Compute the symmetric kernel matrix
	K = exp(-gama * mat_sq_dists)

	# Center the kernel matrix
	N = K.shape[0]
	one_n = np.ones((N, N)) / N
	K = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)

	# Obtaining eigenpairs from the centered kernel matrix scipy.linalg.eigh returns them in ascending order
	eigvals, eigvecs = eigh(K)
	eigvals, eigvecs = eigvals[::-1], eigvecs[:, ::-1]
	# Collect the top k eigenvectors (projected samples)
	X_pc = np.column_stack((eigvecs[:, i] for i  in range(n_components)))
	return X_pc

if __name__ == '__main__':
	# plot half moon
	from sklearn.datasets import make_moons
	X, y = make_moons(n_samples=100, random_state=123)
	fig = plt.figure()
	plt.scatter(X[y==0, 0], X[y==0, 1], color='red', marker='^', alpha=0.5)
	plt.scatter(X[y==1, 0], X[y==1, 1], color='blue', marker='o', alpha=0.5)
	fig.savefig('moon.pdf')

	from sklearn.decomposition import PCA
	scikit_pca = PCA(n_components=2)
	X_spca = scikit_pca.fit_transform(X)
	fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6,4))
	ax[0].scatter(X_spca[y==0, 0], X_spca[y==0, 1], color='red', marker='^', alpha=0.5)
	ax[0].scatter(X_spca[y==1, 0], X_spca[y==1, 1], color='blue', marker='o', alpha=0.5)
	ax[1].scatter(X_spca[y==0, 0], np.zeros((50,1))+0.02, color='red', marker='^', alpha=0.5)
	ax[1].scatter(X_spca[y==1, 0], np.zeros((50,1))-0.02, color='blue', marker='o', alpha=0.5)
	ax[0].set_xlabel('PC1')
	ax[0].set_ylabel('PC2')
	ax[1].set_xlabel('PC1')
	ax[1].set_ylim([-1, 1])
	ax[1].set_yticks([])
	fig.savefig('scikit_PCA.pdf')

	from ML_31_scikitlearn_perceptron import plot_decision_regions 
