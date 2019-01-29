#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import os.path
import numpy as np
import pandas as pd

def scaling(X_train, X_test):
	from sklearn.preprocessing import StandardScaler
	# normalization: range 0-1
	# standerdization:  std = 1
	stdsc = StandardScaler()
	X_train_std = stdsc.fit_transform(X_train)
	X_test_std = stdsc.transform(X_test)
	return X_train_std, X_test_std,

if __name__ == '__main__':
	from ML_04_3_train_test_split import load_data, train_test_spliting
	df = load_data()
	X_train, X_test, y_train, y_test = train_test_spliting(df)

	X_train_std, X_test_std = scaling(X_train, X_test)
