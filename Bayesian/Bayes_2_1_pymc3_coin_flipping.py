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
	np.random.seed(123)
	n_experiments = 4
	theta_real = 0.35
	data = stats.bernoulli.rvs(p=theta_real, size=n_experiments)

	base_name = os.path.basename(__file__)[:-3]
	with pm.Model() as our_first_model,\
			matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		theta = pm.Beta('theta', alpha=1, beta=1)  # prior beta distritibution, to generate numbers
		y = pm.Bernoulli('y', p=theta, observed=data)  # observed= is liklihood

		start = pm.find_MAP()  # maximum a posterieri (MAP)
		step = pm.Metropolis()  # Metropolis-Hastings
		trace = pm.sample(1000, step=step, start=start, njobs=3)

		#  traceplot function to check coverage
		burnin = 100
		chain = trace[burnin:]
		fig = plt.figure()
		pm.traceplot(chain, lines={'theta': theta_real})
		pdf_all.savefig()
		# check coverage quantitatively, Gelman-Rubin test
		result = pm.gelman_rubin(trace)  # Rˆ
		print(result)
		fig = plt.figure()
		pm.forestplot(trace, varnames=['theta'])
		pdf_all.savefig()
		
		# mean, standard deviation, and the HPD intervals
		print(pm.summary(trace))
		
		print(pm.effective_n(trace))

		fig = plt.figure()
		pm.plot_posterior(trace,
				kde_plot=True,
				ref_val=0.5,
				rope=[0.45, 0.55])  # Region Of Practical Equivalence (ROPE)
		pdf_all.savefig()
