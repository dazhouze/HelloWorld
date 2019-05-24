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
	ans = sns.load_dataset('anscombe')
	x_2 = ans[ans.dataset == 'II']['x'].values
	y_2 = ans[ans.dataset == 'II']['y'].values
	x_2 = x_2 - x_2.mean()
	y_2 = y_2 - y_2.mean()

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:

		with pm.Model() as model:
			alpha = pm.Normal('alpha', mu=0, sd=10)
			beta1 = pm.Normal('beta1', mu=0, sd =1)
			beta2 = pm.Normal('beta2', mu=0, sd =1)
			epsilon = pm.Uniform('epsilon', lower=0, upper=10)
			mu = alpha + beta1 * x_2 + beta2 * x_2**2
			y_pred = pm.Normal('y_pred', mu=mu, sd=epsilon, observed=y_2)

			start = pm.find_MAP()
			step = pm.NUTS(scaling=start)
			trace = pm.sample(3000, step=step, start=start,)
			chain = trace[100:]

			fig = plt.figure()
			pm.traceplot(chain)
			pdf_all.savefig()
			
			# mean, standard deviation, and the HPD intervals
			print(pm.summary(trace))
