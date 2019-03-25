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
	theta_real = 0.35
	trials = [0, 1, 2, 3, 4, 8, 16, 32, 50, 150]  #  times of coin flipping
	data = [0, 1, 1, 1, 1, 4, 6, 9, 13, 48]  # times of coin head
	beta_params = [(1, 1), (0.5, 0.5), (20, 20)]
	dist = stats.beta  # prior
	x = np.linspace(0, 1, 100)

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		for idx, N in enumerate(trials):
			fig = plt.figure()
			y = data[idx]
			for (a_prior,b_prior),c in zip(beta_params, ('b', 'r', 'g')):
				p_theta_given_y = dist.pdf(x, a_prior+y, b_prior+N-y)  # p(θ|y)
				plt.plot(x, p_theta_given_y, color=c)
				plt.fill_between(x, 0, p_theta_given_y, color=c, alpha=0.6,
						label= r'$\alpha$: {:.1f} $\beta$: {:.1f}'.format(a_prior, b_prior))
			plt.axvline(theta_real, ymax=0.3, color='k', label= r'$\theta$ real')
			plt.xlim(0,1)
			plt.ylim(0,12)
			plt.xlabel(r'$\theta$', fontsize=20)
			plt.title('{:d} experiments {:d} heads'\
					.format(N, y), fontsize=20)
			plt.legend(frameon=False, fontsize=15)
			plt.gca().axes.get_yaxis().set_visible(False)
			plt.tight_layout()
			pdf_all.savefig()

