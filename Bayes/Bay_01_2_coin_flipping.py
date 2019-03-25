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
	n_params = [1, 2, 4]  # N: number of tosses
	p_params = [0.25, 0.5, 0.75]  # θ: coin head probability 
	x = np.arange(0, max(n_params)+1)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		f, ax = plt.subplots(len(n_params), len(p_params), sharex=True, sharey=True)
		plt.rcParams["font.family"] = 'sans-serif'
		for i in range(3):
			for j in range(3):
				n, p = n_params[i], p_params[j]
				y = stats.binom(n=n, p=p).pmf(x)
				ax[i, j].vlines(x, 0, y, colors='b', lw=5)
				ax[i, j].set_ylim(0, 1)
				ax[i, j].plot(0, 0,
						label='n={:3.2f}\np={:3.2f}'.format(n, p),
						alpha=0)
				ax[i, j].legend(frameon=False, fontsize=10)
		ax[2, 1].set_xlabel('$\\theta$', fontsize=15)
		ax[1,0].set_ylabel('$p(y|\\theta)$', fontsize=14)
		ax[0,0].set_xticks(x)
		pdf_all.savefig()
