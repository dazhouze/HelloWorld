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

	# plot validation curve
	from sklearn.model_selection import validation_curve
	param_range = [0.001, 0.01, 0.1, 1, 10, 100]
	train_scores, test_scores = validation_curve(\
		estimator=pipe_lr, X=X_train, y=y_train, param_name='logisticregression__C',\
		param_range=param_range, cv=10)
	train_mean = np.mean(train_scores, axis=1)
	train_std = np.std(train_scores, axis=1)
	test_mean = np.mean(test_scores, axis=1)
	test_std = np.std(test_scores, axis=1)
	fig = plt.figure()
	plt.plot(param_range, train_mean, color='blue', marker='o', markersize=5, label='training accuracy')
	plt.fill_between(param_range, train_mean+train_std, train_mean-train_std, alpha=0.15, color='blue')
	plt.plot(param_range, test_mean, color='green', marker='s', linestyle='--', markersize=5, label='validation accuracy')
	plt.fill_between(param_range, test_mean+test_std, test_mean-test_std, alpha=0.15, color='green')
	plt.grid()
	plt.xscale('log')
	plt.legend(loc='lower right')
	plt.xlabel('Parameter C')
	plt.ylabel('Accuracy')
	plt.ylim([0.8, 1.03])
	fig.savefig('validation_curve.pdf')

