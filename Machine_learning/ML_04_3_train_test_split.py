#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

def load_data():
	df = pd.read_csv('data/wine.data', header=None)
	df.columns = ['Class label', 'Alcohol',
		'Malic acid', 'Ash',
		'Alcalinity of ash', 'Magnesium',
		'Total phenols', 'Flavanoids',
		'Nonflavanoid phenols',
		'Proanthocyanins',
		'Color intensity', 'Hue',
		'OD280/OD315 of diluted wines',
		'Proline']
	return df
	
def train_test_spliting(df):
	from sklearn.model_selection import train_test_split
	X, y = df.iloc[:, 1:].values, df.iloc[:, 0].values
	X_train, X_test, y_train, y_test =\
			train_test_split(X, y,
					test_size=0.3,
					random_state=0,
					stratify=y)
	return X_train, X_test, y_train, y_test

if __name__ == '__main__':
	df = load_data()
	print(df.head())
	X_train, X_test, y_train, y_test = train_test_spliting(df)
