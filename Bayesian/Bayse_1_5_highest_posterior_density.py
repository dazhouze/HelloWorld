#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns

import numpy as np
from scipy import stats
import os.path

def navie_hpd(post):
	'''
	highest posterior density.
	'''
	sns.kdeplot(post)
	HPD = np.percentile(post,  [2.5, 97.5])
	plt.plot(HPD, [0,0], label='HPD {:.2f} {:.2f}'.format(*HPD), linewidth=8, color='k')
	plt.legend(frameon=False, fontsize=16)
	plt.xlabel(r'$\theta$', fontsize=14)
	plt.gca().axes.get_yaxis().set_ticks([])  # hide y-ticks

if __name__ == '__main__':
	np.random.seed(1)
	# unimodal
	post = stats.beta.rvs(5, 11, size=1000)

	# multi-modal distribution
	gauss_a = stats.norm.rvs(loc=4, scale=0.9, size=3000)
	gauss_b = stats.norm.rvs(loc=-2, scale=1, size=2000)
	max_norm = np.concatenate((gauss_a, gauss_b))

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		# unimodal
		fig = plt.figure()
		navie_hpd(post)
		plt.xlim(0, 1)
		pdf_all.savefig()

		# multi-modal distribution
		fig = plt.figure()
		navie_hpd(max_norm)
		pdf_all.savefig()
