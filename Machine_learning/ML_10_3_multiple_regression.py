#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 


def lin_regplot(X, y, model):
	plt.scatter(X, y, c='blue', s=50, edgecolor='white')
	plt.plot(X, model.predict(X), color='black', lw=2)
	return True

if __name__ == '__main__':
	df = pd.read_csv('housing.data', header=None, sep='\s+')
	df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

	# multiple regression model
	from sklearn.model_selection import train_test_split
	from sklearn.linear_model import LinearRegression
	X = df.iloc[:, :-1].values
	y = df.iloc[:, -1].values  # MEDV
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
	slr = LinearRegression()
	slr.fit(X_train, y_train)
	y_train_pred = slr.predict(X_train)
	y_test_pred = slr.predict(X_test)

	# Residual plots
	fig = plt.figure()
	plt.scatter(y_train_pred, y_train_pred-y_train, c='steelblue', marker='o', edgecolor='white', label='Training data')
	plt.scatter(y_test_pred, y_test_pred-y_test, c='limegreen', marker='s', edgecolor='white', label='Test data')
	plt.xlabel('Predicted values')
	plt.ylabel('Residuals')
	plt.legend(loc='upper left')
	plt.hlines(y=0, xmin=-10, xmax=50, color='black', lw=2)
	fig.savefig('residuals.pdf')

	# Mean Squared Error
	from sklearn.metrics import mean_squared_error
	print('Mean Squared Error of train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred), mean_squared_error(y_test, y_test_pred)))
	print('\tIf train>>test: overfitting.')

	# coefficient of determination (R^2)
	from sklearn.metrics import r2_score
	print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred), r2_score(y_test, y_test_pred)))

	# Ridge regression for regularization
	from sklearn.linear_model import Ridge
	ridge = Ridge(alpha=1)

	# LASSO: Absolute Shrinkage and Selection Operator for regularization
	from sklearn.linear_model import Lasso
	lasso = Lasso(alpha=1)

	# ElasticNet for regularization
	from sklearn.linear_model import ElasticNet
	elanet = ElasticNet(alpha=1, l1_ratio=0.5)
