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
	from io import StringIO
	csv_data = \
			'''A,B,C,D
			1.0,2.0,3.0,4.0
			5.0,6.0,,8.0
			10.0,11.0,12.0,'''
	df = pd.read_csv(StringIO(csv_data))
	print(df)  # missing cell replaced by NaN
	print(df.isnull().sum())  # count the number of missing values per column
	print(df.values)  # pd data frame to np array

	# Eliminating samples or features with missing values
	print(df.dropna(axis=0))
	print(df.dropna(axis=1))

	# replace the missing value with the mean
	from sklearn.preprocessing import Imputer
	imr = Imputer(missing_values='NaN', strategy='mean', axis=0)
	imr = imr.fit(df.values)
	imputed_data = imr.transform(df.values)
	print(imputed_data)
