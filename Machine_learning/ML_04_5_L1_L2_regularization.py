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
