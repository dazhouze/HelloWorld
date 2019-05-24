#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

if __name__ == '__main__':
	from ML_04_3_train_test_split import load_data, train_test_spliting
	df = load_data()
	X_train, X_test, y_train, y_test = train_test_spliting(df)

	from ML_04_4_scaling import scaling
	X_train_std, X_test_std = scaling(X_train, X_test)

	from sklearn.linear_model import LogisticRegression
	lr = LogisticRegression(penalty='l1', C=1.0)
	lr.fit(X_train_std, y_train)
	print('Training accuracy:', lr.score(X_train_std, y_train))
	print('Test accuracy:', lr.score(X_test_std, y_test))

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		colors = ['blue', 'green', 'red', 'cyan',
				'magenta', 'yellow', 'black',
				'pink', 'lightgreen', 'lightblue',
				'gray', 'indigo', 'orange']
		weights, params = [], []
		for c in np.arange(-4, 6):
			lr = LogisticRegression(penalty='l1', C = 10.0**c, random_state=0)
			lr.fit(X_train_std, y_train)
			weights.append(lr.coef_[1])
			params.append(10.0**c)
		weights = np.array(weights)
		fig = plt.figure()
		ax = plt.subplot(111)
		for column, color in zip(range(weights.shape[1]), colors):
			plt.plot(params, weights[:, column],
					label=df.columns[column + 1],
					color=color)
		plt.axhline(0, color='black', linestyle='--', linewidth=3)
		plt.xlim([10**(-5), 10**5])
		plt.ylabel('weight coefficient')
		plt.xlabel('C')
		plt.xscale('log')
		plt.legend(loc='upper left')
		ax.legend(loc='upper center', bbox_to_anchor=(1.38, 1.03), ncol=1, fancybox=True)
		pdf_all.savefig()
