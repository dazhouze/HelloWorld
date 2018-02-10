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

	# RANSAC
	from sklearn.linear_model import LinearRegression
	from sklearn.linear_model import RANSACRegressor
	ransac = RANSACRegressor(LinearRegression(), max_trials=100, min_samples=50, loss='absolute_loss', residual_threshold=5, random_state=1)
	ransac.fit(X, y)
