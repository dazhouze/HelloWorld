#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

class LinearRegressionGD(object):
	def __init__(self, eta=0.001, n_iter=20):
		self.__eta = eta
		self.n_iter = n_iter

	def fit(self, X, y):
		self.__w = np.zeros((2, 1+X.shape[1]))
		self.__cost = []
		for i in range(0, self.n_iter):
			output = self.net_input(X)
			errors = (y - output)
			self.__w[1:] += self.__eta * X.T.dot(errors)  # weight
			self.__w[0] += self.__eta * errors.sum()  # bias
			cost = (errors ** 2).sum()/2
			self.__cost.append(cost)
		return self

	def predict(self, X):
		return self.net_input(X)

	def net_input(self, X):
		return np.dot(X, self.__w[1:]) + self.__w[0]

	def get_cost(self):
		return self.__cost

def lin_regplot(X, y, model):
	plt.scatter(X, y, c='blue', s=50, edgecolor='white')
	plt.plot(X, model.predict(X), color='black', lw=2)
	return True

if __name__ == '__main__':
	df = pd.read_csv('housing.data', header=None, sep='\s+')
	df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
	print(df.head())

	cols = ['LSTAT', 'INDUS', 'NOX', 'RM', 'MEDV']
	fig = sns.pairplot(df[cols], size=2.5)
	plt.tight_layout()
	fig.savefig('pairplot.pdf')
	
	fig = plt.figure()
	cm = np.corrcoef(df[cols].values.T)
	sns.set(font_scale=1.5)
	hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size':15}, yticklabels=cols, xticklabels=cols)
	fig.savefig('corcoeff.pdf')

	# 2 feature linearRegrssion gradient decrease
	X = df[['RM']].values
	y = df[['MEDV']].values
	from sklearn.preprocessing import StandardScaler
	sc_x = StandardScaler()
	sc_y = StandardScaler()
	X_std = sc_x.fit_transform(X)
	y_std = sc_y.fit_transform(y)
	#y_std = sc_y.fit_transform(y[:, np.newaxis]).flatten()
	lr = LinearRegressionGD()
	lr.fit(X_std, y_std)

	fig = plt.figure()
	sns.reset_orig()
	plt.plot(range(1, lr.n_iter+1), lr.get_cost())
	plt.ylabel('SSE')
	plt.xlabel('Epoch')
	fig.savefig('linearRegrssionGD.pdf')

	fig = plt.figure()
	lin_regplot(X_std, y_std, lr)
	plt.xlabel('Averge number of rooms [RM] (standardized)')
	plt.ylabel('Price in $1000s [MEDV] (standardized)')
	fig.savefig('regression.pdf')

	# inverse transform
	num_rooms_std = sc_x.transform([[5.0]])
	price_std = lr.predict(num_rooms_std)
	print('price in $1000: %.3f' % (sc_y.inverse_transform(price_std)[0][0]))

	# estimating coefficient of regression model via scikit-learn
	from sklearn.linear_model import LinearRegression
	slr = LinearRegression()
	slr.fit(X, y)
	print('Slope: %.3f' % slr.coef_[0])
	print('Intercepth: %.3f' % slr.intercept_)
