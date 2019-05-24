#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns

import numpy as np
from scipy import stats
import pymc3 as pm
import os.path

if __name__ == '__main__':
	np.random.seed(314)
	N = 100
	alpha_real = 2.5
	beta_real = [0.9, 1.5]  # two slopes for two independent variables
	eps_real = np.random.normal(0, 0.5, size=N)  # epsilon

	X = np.array([np.random.normal(i, j, N) for i,j in zip([10, 2], [1, 1.5],)])
	X_mean = X.mean(axis=1, keepdims=True)
	X_centered = X - X_mean
	y = alpha_real + np.dot(beta_real, X) + eps_real

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# plot two between each independent variable and the dependent variable 
		fig = plt.figure(figsize=(10, 10))
		for idx, x_i in enumerate(X_centered):
			plt.subplot(2, 2, idx+1)
			plt.scatter(x_i, y)
			plt.xlabel('$x_{}$'.format(idx), fontsize=16)
			plt.ylabel('$y$', rotation=0, fontsize=16)
		plt.subplot(2, 2, idx+2)
		plt.scatter(X_centered[0], X_centered[1])
		plt.xlabel('$x_{}$'.format(idx-1), fontsize=16)
		plt.ylabel('$x_{}$'.format(idx), rotation=0, fontsize=16)
		pdf_all.savefig()

		with pm.Model() as model:
			alpha_tmp = pm.Normal('alpha_tmp', mu=0, sd=10)
			beta = pm.Normal('beta', mu=0, sd =1, shape=2)
			epsilon = pm.HalfCauchy('epsilon', 5)

			mu = alpha_tmp + pm.math.dot(beta, X_centered)
			alpha = pm.Deterministic('alpha', alpha_tmp - pm.math.dot(beta, X_mean))

			y_pred = pm.Normal('y_pred', mu=mu, sd=epsilon, observed=y)

			start = pm.find_MAP()
			step = pm.NUTS(scaling=start)
			trace = pm.sample(5000, step=step, start=start,)
			varnames = ['alpha', 'beta', 'epsilon']
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain, varnames)
			pdf_all.savefig()
			
			# mean, standard deviation, and the HPD intervals
			print(pm.summary(trace))
