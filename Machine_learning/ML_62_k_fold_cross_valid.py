#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
	# 3 steps for raw dataset to training and test datasets
	df = pd.read_csv('wdbc.data', header=None)
	from sklearn.preprocessing import LabelEncoder
	X = df.loc[:, 2:].values
	y = df.loc[:, 1].values
	le = LabelEncoder()
	y = le.fit_transform(y)
	print(le.classes_, '=>', le.transform(le.classes_))
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)

	# chain StandardScaler, PCA and logisticRegression into pipeline
	from sklearn.preprocessing import StandardScaler
	from sklearn.decomposition import PCA
	from sklearn.linear_model import LogisticRegression
	from sklearn.pipeline import make_pipeline
	pipe_lr = make_pipeline(StandardScaler(), PCA(n_components=2), LogisticRegression(random_state=1))
	pipe_lr.fit(X_train, y_train)
	y_pred = pipe_lr.predict(X_test)
	print('Test Accuracy: %.3f\n' % pipe_lr.score(X_test, y_test))

	# stratified k-fold cross-validation
	from sklearn.model_selection import StratifiedKFold
	kfold = StratifiedKFold(n_splits=10, random_state=1).split(X_train, y_train)
	scores = []
	for k,(train, test) in enumerate(kfold):
		pipe_lr.fit(X_train[train], y_train[train])
		score = pipe_lr.score(X_train[test], y_train[test])
		scores.append(score)
		print('Fold: %2d, Class dist.: %s, Acc: %.3f' % (k+1, np.bincount(y_train[train]), score))
	print('\nCV accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
