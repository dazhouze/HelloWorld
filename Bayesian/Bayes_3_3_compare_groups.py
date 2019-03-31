#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns

import numpy as np
import pandas as pd
from scipy import stats
import pymc3 as pm
import os.path

if __name__ == '__main__':

	base_name = os.path.basename(__file__)[:-3]
	with pm.Model() as comparing_groups,\
			matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:

		tips = sns.load_dataset('tips')
		y = tips['tip'].values
		idx = pd.Categorical(tips['day']).codes  # 4 days, 4 groups
		print(set(idx))
		# prior
		means = pm.Normal('means', mu=0, sd=10, shape=len(set(idx)))
		sds = pm.HalfNormal('sds', sd=10, shape=len(set(idx)))
		# likehood
		y = pm.Normal('y', mu=means[idx], sd=sds[idx], observed=y)

		trace = pm.sample(5000, njobs=1)
		chain = trace[100::]
		fig = plt.figure()
		pm.traceplot(chain)
		pdf_all.savefig()
		
		# mean, standard deviation, and the HPD intervals
		print(pm.summary(trace))

		# 
		dist = stats.norm()
		fig, ax = plt.subplots(3, 2, figsize=(16,12))

		comparisons = [(i,j) for i in range(len(set(idx))) for j in range(i+1, len(set(idx)))]
		pos = [(k,l) for k in range(3) for l in (0,1)]

		for (i,j), (k,l) in zip(comparisons, pos):
			means_diff = chain['means'][:,i] - chain['means'][:,j]
			d_cohen = (means_diff / np.sqrt((chain['sds'][:,i]**2 + chain['sds'][:,j]**2)/2) ).mean()

			ps = dist.cdf(d_cohen/(2**0.5))

			pm.plot_posterior(means_diff, ref_val=0, ax=ax[k,l], color='skyblue')
			ax[k,l].plot(0, label="Cohen's d={:.2f}\nPrbo sup={:.2f}".format(d_cohen, ps), alpha=0)
			ax[k,l].set_xlabel('$\mu_{}-\mu_{}$'.format(i, j), fontsize=15)
			ax[k,l ].legend(loc=0, fontsize=14)
		pdf_all.savefig(fig)
