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
	data = np.array([51.06, 55.12, 53.73, 50.24, 52.05, 56.40, 48.45,
	52.34, 55.65, 51.49, 51.86, 63.43, 53.00, 56.09, 51.93, 52.31, 52.33,
	57.48, 57.44, 55.14, 53.93, 54.62, 56.09, 68.58, 51.36, 55.47, 50.73,
	51.94, 54.95, 50.39, 52.91, 51.5, 52.68, 47.72, 49.73, 51.82, 54.99,
	52.84, 53.19, 54.52, 51.46, 53.73, 51.61, 49.81, 52.42, 54.3, 53.84,
	53.16])
	print(data.shape)

	base_name = os.path.basename(__file__)[:-3]
	with pm.Model() as model_g,\
			matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
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
