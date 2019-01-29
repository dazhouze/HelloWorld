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
	df = pd.DataFrame([
		['green', 1, 10.1, 'class1'],
		['red', 2, 13.5, 'class2'],
		['blue', 3, 15.3, 'class1']
		])
	df.columns = ['color', 'size', 'price', 'classlabel']

	X = df[['color', 'size', 'price',]].values
	print(X)
	from sklearn.preprocessing import LabelEncoder
	X[:, 0] = LabelEncoder().fit_transform(X[:, 0])
	print(X)

	# sklearn's one-hot encoding
	from sklearn.preprocessing import OneHotEncoder
	ohe = OneHotEncoder(categorical_features=[0])
	X = ohe.fit_transform(X).toarray()
	print(X)

	# pd's one-hot encoding
	X = pd.get_dummies(df[['price', 'color', 'size']])
	print(X)
