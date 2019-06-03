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
import theano.tensor as tt

if __name__ == '__main__':
	iris = sns.load_dataset('iris')
	y = pd.Categorical(iris['species']).codes
	x = iris[iris.columns[:-1]].values
	x = (x - x.mean(axis=0))/x.std(axis=0)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		with pm.Model() as model:
			alpha = pm.Normal('alpha', mu=0, sd=2, shape=3)
			beta = pm.Normal('beta', mu=0, sd=2, shape=(4,3))  # shape
			mu = alpha + pm.math.dot(x, beta)
			theta = tt.nnet.softmax(mu)

			yl = pm.Categorical('yl', theta, observed=y)
			start, step = pm.find_MAP(), pm.NUTS()
			trace = pm.sample(2000, step=step, start=start,)
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain)
			pdf_all.savefig()
	
			# prediction
			data_pred = trace['alpha'].mean(axis=0) + np.dot(x, trace['beta'].mean(axis=0))
			y_pred = []
			for point in data_pred:
				y_pred.append(np.exp(point)/np.sum(np.exp(point), axis=0))
			correct = np.sum(y == np.argmax(y_pred, axis=1)) / len(y)
			print(correct)

		# extra parameters
		with pm.Model() as model:
			alpha = pm.Normal('alpha', mu=0, sd=2, shape=2)
			beta = pm.Normal('beta', mu=0, sd=2, shape=(4,2))  # shape

			alpha_f = tt.concatenate([[0] , alpha])
			beta_f = tt.concatenate([np.zeros((4,1)) , beta], axis=1)

			mu = alpha_f + pm.math.dot(x, beta_f)
			theta = tt.nnet.softmax(mu)

			yl = pm.Categorical('yl', theta, observed=y)
			start, step = pm.find_MAP(), pm.NUTS()
			trace = pm.sample(2000, step=step, start=start,)
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain)
			pdf_all.savefig()
