#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

if __name__ == '__main__':
	df = pd.read_csv('housing.data', header=None, sep='\s+')
	df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

	# decision tree
	from sklearn.tree import DecisionTreeRegressor
	X = df[['LSTAT']].values
	y = df['MEDV'].values
	tree = DecisionTreeRegressor(max_depth=3)
	tree.fit(X, y)
	sort_idx = X.flatten().argsort()
	fig = plt.figure()

	plt.scatter(X[sort_idx], y[sort_idx], c='blue', s=50, edgecolor='white')
	plt.plot(X[sort_idx], tree.predict(X[sort_idx]), color='black', lw=2)

	plt.xlabel('% lower status of the population [LATAT]')
	plt.ylabel('Price in $1000s [MEDV]')
	fig.savefig('decision_tree.pdf')

	# random forest
	X = df.iloc[:, :-1].values
	y = df['MEDV'].values
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)
	from sklearn.ensemble import RandomForestRegressor
	forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=1, n_jobs=10)
	forest.fit(X_train, y_train)
	y_train_pred = forest.predict(X_train)
	y_test_pred = forest.predict(X_test)
	from sklearn.metrics import mean_squared_error
	from sklearn.metrics import r2_score
	print('MSE of train: %.4f, test: %.4f' % (mean_squared_error(y_train, y_train_pred), mean_squared_error(y_test, y_test_pred)))
	print('R^2 train: %.4f, test: %.4f' % (r2_score(y_train, y_train_pred), r2_score(y_test, y_test_pred)))

	fig = plt.figure()
	plt.scatter(y_train_pred, y_train_pred - y_train, c='steelblue', edgecolor='white', marker='o', s=35, alpha=0.9, label='Training data')
	plt.scatter(y_test_pred, y_test_pred-y_test, c='limegreen', edgecolor='white', marker='s', s=35, alpha=0.9, label='Test data')
	plt.xlabel('Predicted values')
	plt.ylabel('Residuals')
	plt.legend(loc='upper left')
	plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='black')
	plt.xlim([-10, 50])
	fig.savefig('Residuals_of_forest.pdf')
