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
	params = [0.5, 1, 2, 3]
	x = np.linspace(0, 1, 100)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		f, ax = plt.subplots(len(params), len(params), sharex=True, sharey=True)
		plt.rcParams["font.family"] = 'sans-serif'
		for i in range(4):
			for j in range(4):
				a, b = params[i], params[j]  # α and β
				y = stats.beta(a, b).pdf(x)
				ax[i,j].plot(x, y, color='b',)
				ax[i,j].plot(0, 0,
						label='$\\alpha$={:3.2f}\n$\\beta$={:3.2f}'.format(a, b),
						alpha=0)
				ax[i,j].legend(frameon=False, fontsize=10)
		ax[3,2].set_xlabel('$\\theta$', fontsize=15)
		ax[1,0].set_ylabel('$p(y|\\theta)$', fontsize=14)
		pdf_all.savefig()
