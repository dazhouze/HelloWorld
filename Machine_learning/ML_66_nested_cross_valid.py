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

	# ROC AUC
	from sklearn.metrics import roc_curve, auc
	from scipy import interp
	pipe_lr = make_pipeline(StandardScaler(), PCA(n_components=2), LogisticRegression(penalty='l2', random_state=1, C=1000))
	X_train2 = X_train[:, [4, 14]]
	from sklearn.model_selection import StratifiedKFold
	cv = list(StratifiedKFold(n_splits=3, random_state=1).split(X_train, y_train))
	fig = plt.figure(figsize=(7, 5))
	mean_tpr = 0
	mean_fpr = np.linspace(0, 1, 100)
	all_tpr = []
	for i,(train, test) in enumerate(cv):
		probas = pipe_lr.fit(X_train2[train], y_train[train]).predict_proba(X_train2[test])
		fpr, tpr, thresholds = roc_curve(y_train[test], probas[:, 1], pos_label=1)
		mean_tpr += interp(mean_fpr, fpr, tpr)
		mean_tpr[0] = 0.0
		roc_auc = auc(fpr, tpr)
		plt.plot(fpr, tpr, label='ROC fold %d (area =  %.2f)' % (i+1, roc_auc))
	plt.plot([0, 1], [0, 1], linestyle='--', color=(0.6,0.6,0.6), label='random guessing')
	mean_tpr /= len(cv)
	mean_tpr[-1] = 1
	mean_auc = auc(mean_fpr, mean_tpr)
	plt.plot(mean_fpr, mean_tpr, 'k--', label='mean ROC (area = %0.2f)' % mean_auc, lw=2)
	plt.plot([0, 0, 1], [0, 1, 1], linestyle=':', color='black', label='perfect performance')
	plt.xlim([-0.05, 1.05])
	plt.ylim([-0.05, 1.05])
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
	plt.legend(loc='lower right')
	fig.savefig('ROC.pdf')

