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

	x = np.random.normal(10, 1, 100)
	y_real = 2.5 + 0.9 * x
	y = y_real + np.random.normal(0, 0.5, size=100)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all,\
			pm.Model() as model:
		# prior
		alpha = pm.Normal('alpha', mu=0, sd=10)  # α
		beta = pm.Normal('beta', mu=0, sd=1)  # β
		epsilon = pm.HalfCauchy('epsilon', 5)  # σ

		# likehood
		mu = alpha + beta * x
		y_pred = pm.Normal('y_pred', mu=mu, sd=epsilon, observed=y)

		rb = pm.Deterministic('rb', (beta * x.std() / y.std()) ** 2)

		y_mean = y.mean()
		ss_reg = pm.math.sum((mu - y_mean) ** 2)
		ss_tot = pm.math.sum((y - y_mean) ** 2)
		rss = pm.Deterministic('rss', ss_reg/ss_tot)

		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(2000,  step=step, start=start)

		chain = trace[200:]
		fig = plt.figure()
		pm.traceplot(chain)
		pdf_all.savefig()

		# Pearson coefficient from a multivariate Gaussian
		sigma_x1 = 1  # ∑
		sigmas_x2 = [1, 2]  # ∑
		rhos = [-0.99, -0.5, 0, 0.5, 0.99]  # ρ
		x, y = np.mgrid[-5:5:0.1, -5:5:0.1]
		pos = np.empty(x.shape + (2,))
		pos[:, :, 0], pos[:, :, 1] = x, y

		fig, ax = plt.subplots(len(sigmas_x2), len(rhos), sharex=True, sharey=True)
		for i in range(2):
			for j in range(5):
				sigma_x2, rho = sigmas_x2[i], rhos[j]
				cov = [[sigma_x1**2, sigma_x1*sigma_x2*rho], 
						[sigma_x1*sigma_x2*rho, sigma_x2**2]]
				rv = stats.multivariate_normal([0, 0], cov)
				ax[i, j].contour(x, y, rv.pdf(pos))
				ax[i, j].plot(0, 0, 
						label='$\\sigma_{{x2}}$={:3.2f}\n$\\rho$={:3.2f}'.format(sigma_x2, rho),
						alpha=0)
				ax[i, j].legend(frameon=False)
		ax[1,2].set_xlabel('$x_1$')
		ax[1,0].set_ylabel('$x_2$')
		pdf_all.savefig(fig)

		# 
		with pm.Model() as model:
			mu = pm.Normal('mu', mu=y, sd=10, shape=2)
			sigma_1 = pm.HalfNormal('sigma_1', 10)
			sigma_2 = pm.HalfNormal('sigma_2', 10)
			rho = pm.Uniform('rho', -1, 1)

			cov = pm.match.stack(([sigma_1**2, sigma_1*sigma_2*rho],
				[sigma_1*sigma_2*rho, sigma_2**2]))
			y_pred = pm.MvNormal('y_pred', mu=mu, cov=cov, observed=y)
			start = pm.find_MAP()
			step = pm.NUTS(scaling=start)
			trace = pm.sample(1000, step=step, start=start)

		chain = trace[200:]
		fig = plt.figure()
		pm.traceplot(chain)
		pdf_all.savefig()

