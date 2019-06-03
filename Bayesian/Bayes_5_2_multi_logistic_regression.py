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
import pandas as pd

if __name__ == '__main__':
	iris = sns.load_dataset('iris')
	df = iris.query('species == ("setosa", "versicolor")')

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
	
		# Multiple logistic regression
		y = pd.Categorical(df['species']).codes
		x = df[['sepal_length', 'sepal_width']].values
		with pm.Model() as model:
			alpha = pm.Normal('alpha', mu=0, sd=10)
			beta = pm.Normal('beta', mu=0, sd=2, shape=2)  # shape
			
			mu = alpha + pm.math.dot(x, beta)
			theta = pm.Deterministic('theta', 1/(1+pm.math.exp(-mu)))  # result of apply logistic func to varible mu
			bd = pm.Deterministic('bd', -alpha/beta[1] - beta[0]/beta[1]*x[:,0])  # boyndary decision

			yl = pm.Bernoulli('yl', theta, observed=y)
			start, step = pm.find_MAP(), pm.NUTS()
			trace = pm.sample(5000, step=step, start=start,)
			varnames = ['alpha', 'beta', 'bd']
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain, varnames)
			pdf_all.savefig()

		idx = np.argsort(x[:,0])
		bd = chain['bd'].mean(0)[idx]
		plt.scatter(x[:,0], x[:,1], c=y)
		plt.plot(x[:,0][idx], bd, color='r');
		bd_hpd = pm.hpd(chain['bd'])[idx]
		plt.fill_between(x[:,0][idx], bd_hpd[:,0], bd_hpd[:,1], color='r', alpha=0.5);
		plt.xlabel('sepal_length', fontsize=16)
		plt.ylabel('sepal_width', fontsize=16)
	
