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

	# plot validation curve
	from sklearn.model_selection import GridSearchCV
	from sklearn.svm import SVC
	pipe_svc = make_pipeline(StandardScaler(), SVC(random_state=1))
	param_range = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
	param_grid = [{'svc__C': param_range, 'svc__kernel': ['linear']},\
			{'svc__C': param_range, 'svc__gamma': param_range, 'svc__kernel': ['rbf']}]
	gs = GridSearchCV(estimator=pipe_svc, param_grid=param_grid, scoring='accuracy', cv=10, n_jobs=4)
	gs = gs.fit(X_train, y_train)
	print(gs.best_score_)
	print(gs.best_params_)

	clf = gs.best_estimator_
	clf.fit(X_train, y_train)
	print('Test accuracy: %.3f' % clf.score(X_test, y_test))
