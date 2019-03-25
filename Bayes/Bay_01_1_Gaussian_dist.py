#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
from scipy import stats
import os.path

if __name__ == '__main__':
	mu_params = [-1, 0, 1]  # μ, mean
	sd_params = [0.5, 1, 1.5]   # σ, standard deviation
	x = np.linspace(-7, 7, 100)  # Return evenly spaced numbers over a specified interval

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		f, ax = plt.subplots(len(mu_params), len(sd_params), sharex=True, sharey=True)
		for i in range(3):
			for j in range(3):
				mu = mu_params[i]
				sd = sd_params[j]
				y = stats.norm(mu, sd).pdf(x)
				ax[i, j].plot(x, y,
						)
				ax[i, j].plot(0, 0,
						label = '$\\mu$ = {:3.2f}\n$\\sigma$ = {:3.2f}'.format(mu, sd),
						alpha=0)
				ax[i, j].legend(frameon=False, fontsize=12)
		ax[2,1].set_xlabel('$x$', fontsize=16)
		ax[1,0].set_ylabel('$pdf(x)$', fontsize=16)
		plt.tight_layout()
		pdf_all.savefig()
