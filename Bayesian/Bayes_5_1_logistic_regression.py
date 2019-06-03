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

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure(figsize=(10, 10))
		sns.stripplot(x="species", y="sepal_length", data=iris, jitter=True)
		pdf_all.savefig()
		fig = plt.figure(figsize=(10, 10))
		sns.pairplot(iris, hue='species', diag_kind='kde')
		pdf_all.savefig()

		# single regression
		df = iris.query("species == ('setosa', 'versicolor')")
		y = pd.Categorical(df['species']).codes
		x = df['sepal_length'].values

		with pm.Model() as model:
			alpha = pm.Normal('alpha', mu=0, sd=10)
			beta = pm.Normal('beta', mu=0, sd=10)
			
			mu = alpha + pm.math.dot(x, beta)
			theta = pm.Deterministic('theta', 1/(1+pm.math.exp(-mu)))  # result of apply logistic func to varible mu
			bd = pm.Deterministic('bd', -alpha/beta)  # boyndary decision

			yl = pm.Bernoulli('yl', theta, observed=y)
			start, step = pm.find_MAP(), pm.NUTS()
			trace = pm.sample(5000, step=step, start=start,)
			varnames = ['alpha', 'beta', 'bd']
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain, varnames)
			pdf_all.savefig()
			
			# mean, standard deviation, and the HPD intervals
			print(pm.summary(trace))

			#fig = plt.figure()
			#theta = trace['theta'].mean(axis=0)
			#print(theta)
			#idx = np.argsort(x)

			#plt.plot(x[idx], theta[idx], color='b', lw=3);
			#plt.axvline(trace['bd'].mean(), ymax=1, color=''r'')
			#bd_hpd = pm.hpd(trace['bd'])
			#plt.fill_betweenx([0, 1], bd_hpd[0], bd_hpd[1], color='r', alpha=0.5)

			#plt.plot(x, y, 'o', color='k')
			#theta_hpd = pm.hpd(trace['theta'])[idx]
			#plt.fill_between(x[idx], theta_hpd[:,0], theta_hpd[:,1], color='b', alpha=0.5)

			#plt.xlabel('sepal_length', fontsize=16)
			#plt.ylabel(r'$\theta$', rotation=0, fontsize=16)
			#pdf_all.savefig()

