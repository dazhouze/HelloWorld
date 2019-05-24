#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

'''
columns 1 in wine dataset:
 	1) Alcohol
 	2) Malic acid
 	3) Ash
	4) Alcalinity of ash
 	5) Magnesium
	6) Total phenols
 	7) Flavanoids
 	8) Nonflavanoid phenols
 	9) Proanthocyanins
	10)Color intensity
 	11)Hue
 	12)OD280/OD315 of diluted wines
 	13)Proline
'''

if __name__ == '__main__':
   
	from ML_04_3_train_test_split import load_data, train_test_spliting
	df = load_data()
	X_train, X_test, y_train, y_test = train_test_spliting(df)

	#  Random Forest
	feat_labels = df.columns[1:]
	forest = RandomForestClassifier(n_estimators=500, random_state=1)
	forest.fit(X_train, y_train)
	importances = forest.feature_importances_

	indices = np.argsort(importances)[::-1]

	for f in range(X_train.shape[1]):
		print('{:2d}) {} {}'.format(f+1, 30, feat_labels[indices[f]], importances[indices[f]]))
	
	# SelectFromModel
	sfm = SelectFromModel(forest, threshold=0.1, prefit=True)
	X_selected = sfm.transform(X_train)
	print('Number of samples that meet this criterion:', X_selected.shape[0])
	for f in range(X_selected.shape[1]):
		print('{:2d}) {} {}'.format(f+1, feat_labels[indices[f]], importances[indices[f]]))

	base_name = os.path.basename(__file__)[:-3]
	with matplotlib.backends.backend_pdf.PdfPages('%s.pdf' % base_name) as pdf_all:
		fig = plt.figure()
		plt.title('Feature Importance')
		plt.bar(range(X_train.shape[1]),
				importances[indices],
				align='center')
		plt.xticks(range(X_train.shape[1]),
				feat_labels, rotation=90)
		plt.xlim([-1, X_train.shape[1]])
		pdf_all.savefig()

