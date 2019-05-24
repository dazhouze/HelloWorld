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
	rates = [1, 2, 5]
	scales = [1, 2, 3]
	x = np.linspace(0, 20, 100)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:

		# gamma distribution
		fig, ax = plt.subplots(len(rates), len(scales), sharex=True, sharey=True)
		ax[0, 1].set_title('$gamma$ distribution')
		for i in range(len(rates)):
			for j in range(len(scales)):
				rate, scale = rates[i], scales[j]
				y = stats.gamma(a=rate, scale=scale).pdf(x)
				ax[i, j].plot(x, y,
						label='$\\alpha$={:3.2f}\n$\\theta$={:3.2f}'.format(rate, scale))
				ax[i, j].legend(frameon=False)
		ax[2, 1].set_xlabel('$x$')
		ax[1, 0].set_ylabel('$pdf(x)$')
		pdf_all.savefig(fig)

		# y ∼ N (μ = α + β x,σ = ε )
		np.random.seed(314)
		N = 100
		alfa_real = 2.5  # α
		beta_real = 0.9  # β
		eps_real = np.random.normal(0, 0.5, size=N)  # σ

		x = np.random.normal(10, 1, N)
		y_real = alfa_real + beta_real * x
		y = y_real + eps_real

		fig, ax = plt.subplots(1, 2)
		ax[0].scatter(x, y, color='b')
		ax[0].plot(x, y_real, color='k')
		ax[0].set_xlabel('$x$', fontsize=15)
		ax[0].set_ylabel('$y$', fontsize=15)
		sns.kdeplot(y, ax = ax[1])
		ax[1].set_xlabel('$y$', fontsize=15)
		pdf_all.savefig(fig)


		with pm.Model() as model:
			# prior
			alpha = pm.Normal('alpha', mu=0, sd=10)  # α
			beta = pm.Normal('beta', mu=0, sd=1)  # β
			epsilon = pm.HalfCauchy('epsilon', 5)  # σ

			# likehood
			#y_pred = pm.Normal('y_pred', mu=alpha + beta*x, sd=epsilon, observed=y)
			mu = pm.Deterministic('mu', alpha + beta*x)
			y_pred = pm.Normal('y_pred', mu=mu, sd=epsilon, observed=y)
			start = pm.find_MAP()
			step = pm.Metropolis()
			trace = pm.sample(1000, step=step, start=start, njobs=1)

		chain = trace[200:]
		fig = plt.figure()
		pm.traceplot(chain)
		pdf_all.savefig()
		fig = plt.figure()
		pm.autocorrplot(trace, ['alpha', 'beta', 'epsilon'])
		pdf_all.savefig()

		# mean, standard deviation, and the HPD intervals
		print(pm.summary(trace))

		fig = plt.figure()
		sns.kdeplot(trace['alpha'], trace['beta'])
		plt.xlabel(r'$\alpha$', fontsize=15)
		plt.ylabel(r'$\beta$', fontsize=15, rotation=0)
		pdf_all.savefig(fig)

		# Interpreting and visualizing the posterior
		fig = plt.figure()
		plt.title('visualizing the posterior', fontsize=20)
		plt.scatter(x, y, color='b')
		alpha_m = trace['alpha'].mean()
		beta_m = trace['beta'].mean()
		plt.plot(x, alpha_m + beta_m*x, color='k', label='y={:.2f}+{:.3f}*x'.format(alpha_m, beta_m))
		plt.xlabel('$x$', fontsize=15)
		plt.ylabel('$y$', fontsize=15, rotation=0)
		plt.legend(loc=2, fontsize=15, frameon=False)
		pdf_all.savefig(fig)

		# sampling from posterior
		fig = plt.figure()
		plt.title('sampling from posterior', fontsize=20)
		plt.scatter(x, y, color='b')
		idx = range(0, len(trace['alpha']), 10)
		# sampling from posterior
		plt.plot(x,
				trace['alpha'][idx] + trace['beta'][idx]*x[:,np.newaxis],
				color='grey',
				alpha=0.5)
		# real
		plt.plot(x,
				alpha_m + beta_m*x,
				color='k',
				label='y={:.2f}+{:.2f}*x'.format(alpha_m, beta_m))
		plt.xlabel('$x$', fontsize=15)
		plt.ylabel('$y$', fontsize=15, rotation=0)
		plt.legend(loc=2, fontsize=15, frameon=False)
		pdf_all.savefig(fig)

		# show Highest Posterior Density
		fig = plt.figure()
		plt.title('Highest Posterior Density (HPD)', fontsize=20)
		plt.scatter(x, y, color='b')
		plt.plot(x, alpha_m + beta_m*x, color='k', label='y={:.2f}+{:.3f}*x'.format(alpha_m, beta_m))
		idx = np.argsort(x)
		x_ord = x[idx]
		sig = pm.hpd(trace['mu'], alpha=0.02)[idx]
		plt.fill_between(x_ord, sig[:,0], sig[:,1], color='grey', alpha=0.5)
		plt.xlabel('$x$', fontsize=15)
		plt.ylabel('$y$', fontsize=15, rotation=0)
		plt.legend(loc=2, fontsize=15, frameon=False)
		pdf_all.savefig(fig)

		# a darker gray for the HPD 50 and a lighter gray for the HPD 95
		ppc = pm.sampling.sample_posterior_predictive(chain, samples=1000, model=model) # posterior predictive samples
		fig = plt.figure()
		plt.title('Highest Posterior Density (HPD)\ndarker gray for the HPD 50\nand lighter gray for the HPD 95', fontsize=20)
		plt.scatter(x, y, color='b')
		plt.plot(x, alpha_m + beta_m*x, color='k', label='y={:.2f}+{:.3f}*x'.format(alpha_m, beta_m))
		sig0 = pm.hpd(ppc['y_pred'], alpha=0.5)[idx]  # 50 HPD
		sig1 = pm.hpd(ppc['y_pred'], alpha=0.05)[idx]   # 95 HPD
		plt.fill_between(x_ord, sig0[:,0], sig0[:,1], color='grey', alpha=0.8)
		plt.fill_between(x_ord, sig1[:,0], sig1[:,1], color='grey', alpha=0.5)
		plt.xlabel('$x$', fontsize=15)
		plt.ylabel('$y$', fontsize=15, rotation=0)
		plt.legend(loc=2, fontsize=15, frameon=False)
		pdf_all.savefig(fig)


