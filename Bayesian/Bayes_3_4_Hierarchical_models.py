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
	# the synthetic data, three groups,
	N_samples = [30, 30, 30]  # total number of each groups
	G_samples = [18, 18, 18]  # record of the number of good-quality samples

	group_idx = np.repeat(np.arange(len(N_samples)), N_samples)
	data = []
	for i in range(0, len(N_samples)):
		data.extend(np.repeat([1, 0], [G_samples[i], N_samples[i]-G_samples[i]]))
	print(group_idx, data)

	base_name = os.path.basename(__file__)[:-3]
	with pm.Model() as model_h,\
			matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# prior
		alpha = pm.HalfCauchy('alpha', beta=10)
		beta = pm.HalfCauchy('beta', beta=10)
		theta = pm.Beta('theta', alpha, beta, shape=len(N_samples))

		# likehood
		y = pm.Bernoulli('y', p=theta[group_idx], observed=data)

		trace = pm.sample(2000, njobs=1)

		chain = trace[200:]
		fig = plt.figure()
		pm.traceplot(chain)
		pdf_all.savefig()
		
		# mean, standard deviation, and the HPD intervals
		print(pm.summary(trace))

