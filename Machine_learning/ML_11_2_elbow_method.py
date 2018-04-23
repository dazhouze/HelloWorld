#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

if __name__ == '__main__':
	from sklearn.datasets import make_blobs
	X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)

	from sklearn.cluster import KMeans
	km = KMeans(n_clusters=3, init='random', n_init=10, max_iter=300, tol=1e-04, random_state=0)
	
	distortions = []
	for i in range(1, 11):
		km  = KMeans(n_clusters=i, init='k-means++', n_init=300, random_state=0)
		km.fit(X)
		distortions.append(km.inertia_)

	fig = plt.figure()
	plt.plot(range(1, 11), distortions, marker='o')
	plt.xlabel('Number of clusters')
	plt.ylabel('Distortion')
	fig.savefig('Distortion.pdf')
