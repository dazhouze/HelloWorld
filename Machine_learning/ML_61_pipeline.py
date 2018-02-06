#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
	# 3 steps for raw dataset to training and test datasets
	df = pd.read_csv('wdbc.data', header=None)
	from sklearn.preprocessing import LabelEncoder
	X = df.loc[:, 2:].values
	y = df.loc[:, 1].values
	le = LabelEncoder()
	y = le.fit_transform(y)
	print(le.classes_, '=>', le.transform(le.classes_))
	from sklear.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)

    from sklearn.preprocessing import StandardScaler
