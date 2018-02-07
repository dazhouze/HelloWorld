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
	pipe_lr = make_pipeline(StandardScaler(), LogisticRegression(penalty='l2', random_state=1))  # regulation penalty

	# plot learning curve
	from sklearn.model_selection import learning_curve
	train_sizes, train_scores, test_scores =\
		learning_curve(estimator=pipe_lr, X=X_train, y=y_train,\
		train_sizes=np.linspace(0.1, 1, 10),cv=10, n_jobs=1)

	train_mean = np.mean(train_scores, axis=1)
	train_std = np.std(train_scores, axis=1)
	test_mean = np.mean(test_scores, axis=1)
	test_std = np.std(test_scores, axis=1)

	fig = plt.figure()
	plt.plot(train_sizes, train_mean, color='blue', marker='o', markersize=5, label='training accuracy')
	plt.fill_between(train_sizes, train_mean+train_std, train_mean-train_std, alpha=0.15, color='blue')
	plt.plot(train_sizes, test_mean, color='green', linestyle='--', marker='s', markersize=5, label='validation accuracy')
	plt.fill_between(train_sizes, test_mean+test_std, test_mean-test_std, alpha=0.15, color='green')
	plt.grid()
	plt.xlabel('Number of training samples')
	plt.ylabel('Accuracy')
	plt.legend(loc='lower right')
	plt.ylim([0.85, 1.1])
	plt.savefig('learning_curve.pdf')
