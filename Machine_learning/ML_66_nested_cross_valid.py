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
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1)

	# chain StandardScaler, PCA and logisticRegression into pipeline
	from sklearn.preprocessing import StandardScaler
	from sklearn.decomposition import PCA
	from sklearn.linear_model import LogisticRegression
	from sklearn.pipeline import make_pipeline

	# 5*2 cross-validation
	from sklearn.model_selection import GridSearchCV
	from sklearn.svm import SVC
	pipe_svc = make_pipeline(StandardScaler(), SVC(random_state=1))
	param_range = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
	param_grid = [{'svc__C': param_range, 'svc__kernel': ['linear']},\
			{'svc__C': param_range, 'svc__gamma': param_range, 'svc__kernel': ['rbf']}]
	gs = GridSearchCV(estimator=pipe_svc, param_grid=param_grid, scoring='accuracy', cv=2)
	from sklearn.model_selection import cross_val_score
	scores = cross_val_score(gs, X_train, y_train, scoring='accuracy', cv=5)
	print('SVM CV accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
	gs = gs.fit(X_train, y_train)

	# decision tree
	from sklearn.tree import DecisionTreeClassifier
	gs = GridSearchCV(estimator=DecisionTreeClassifier(random_state=0),\
		param_grid=[{'max_depth': [1,2,3,4,5,6,7, None]}], scoring='accuracy', cv=2)
	scores = cross_val_score(gs, X_train, y_train, scoring='accuracy', cv=5)
	print('Decision tree CV accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))

	# confusion matrix
	from sklearn.metrics import confusion_matrix
	pipe_svc.fit(X_train, y_train)
	y_pred = pipe_svc.predict(X_test)
	confmat =  confusion_matrix(y_true=y_test, y_pred=y_pred)
	print(confmat)
	fig, ax = plt.subplots(figsize=(2.5, 2.5))
	ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)
	for i in range(confmat.shape[0]):
		for j in range(confmat.shape[1]):
			ax.text(x=j, y=i, s=confmat[i, j], va='center', ha='center')
	plt.xlabel('predicted label')
	plt.ylabel('true lable')
	fig.savefig('confusion_matrix.pdf')

	# other metrics 
	from sklearn.metrics import precision_score
	from sklearn.metrics import recall_score, f1_score
	print('Precision: %.3f' % precision_score(y_true=y_test, y_pred=y_pred))
	print('Recall: %.3f' % recall_score(y_true=y_test, y_pred=y_pred))
	print('F1: %.3f' % f1_score(y_true=y_test, y_pred=y_pred))
