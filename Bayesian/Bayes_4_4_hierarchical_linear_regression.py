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

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		N = 20
		M = 8
		idx = np.repeat(range(M-1), N)
		idx = np.append(idx, 7)
		alpha_real = np.random.normal(2.5, 0.5, size=M)
		beta_real = np.random.beta(60, 10, size=M)
		eps_real = np.random.normal(0, 0.5, size=len(idx))

		y_m = np.zeros(len(idx))
		x_m = np.random.normal(10, 1, len(idx))
		y_m = alpha_real[idx] + beta_real[idx]*x_m + eps_real

		# data
		#j, k = 0, N
		#for i in range(M):
		#	plt.subplot(2, 4, i+1)
		#	plt.scatter(x_m[j:k], y_m[j:k])
		#	plt.xlim(6, 15)
		#	plt.ylim(7, 17)
		#	j += N
		#	k += N
		#plt.tight_layout()

		with pm.Model() as model,\
			mu = pm.Uniform('mu', 40, 75)
			sigma = pm.HalfNormal('sigma', sd=10)
			y = pm.Normal('y', mu=mu, sd=sigma, observed=data)
		
			trace_g = pm.sample(1100, njobs=4)
			pm.sample
			chain_g = trace_g[100:]
			fig = plt.figure()
			pm.traceplot(chain_g)
			pdf_all.savefig()
			
			# mean, standard deviation, and the HPD intervals
			print(pm.summary(trace_g))
		
			# posterior predictive checks
			#y_pred = pm.sampling.sample_posterior_predictive(chain_g, 100, model_g, size=40)
			y_pred = pm.sampling.sample_posterior_predictive(chain_g, 100, model_g)
			print(np.shape(y_pred['y']))
			fig = plt.figure()
			sns.kdeplot(data, color='b')
			for i in y_pred['y']:
				sns.kdeplot(i, color='r', alpha=0.1)
			plt.xlim(35, 75)
			plt.title('Gaussian model', fontsize=16)
			plt.xlabel('$x$', fontsize=16)
			pdf_all.savefig()
