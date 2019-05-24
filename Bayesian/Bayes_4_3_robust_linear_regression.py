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
		ans = sns.load_dataset('anscombe')
		x_3 = ans[ans.dataset=='III']['x'].values
		y_3 = ans[ans.dataset=='III']['y'].values
		fig, ax = plt.subplots(1, 2, figsize=(10,5))
		beta_c, alpha_c = stats.linregress(x_3, y_3)[:2]
		ax[0, 1].plot(x_3, (alpha_c + beta_c* x_3), 'k',
				label='y ={:.2f} + {:.2f} * x'.format(alpha_c, beta_c))



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
