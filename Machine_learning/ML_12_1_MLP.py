#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 
import os
import struct
import sys


if __name__ == '__main__':
	'''
	# load data and compress into npz
	import tensorflow.examples.tutorials.mnist.input_data
	from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
	mnist = read_data_sets("MNIST_data/", one_hot=True)
	X_train, X_test, y_train, y_test = mnist.train.images, mnist.test.images, mnist.train.labels, mnist.test.labels
	print('Rows: %d, columns: %d' % (X_train.shape[0], X_train.shape[1]))
	print('Rows: %d, columns: %d' % (X_test.shape[0], X_test.shape[1]))
	print(y_train[0])

	fig, ax = plt.subplots(nrows=2, ncols=5, sharex=True, sharey=True)
	ax = ax.flatten()
	for i in range(10):
		X_train[0].reshape(28, 28)
		for xt,yt in zip(X_train,y_train):
			if np.argmax(yt)==i: 
				img = xt.reshape(28,28)
				break
		img = img.reshape(28, 28)
		ax[i].imshow(img, cmap='Greys')
	ax[0].set_xticks([])
	ax[0].set_yticks([])
	plt.tight_layout()
	fig.savefig('mnist_0_9.pdf')

	y_train=np.argmax(y_train, axis=1)
	y_test=np.argmax(y_test, axis=1)
	np.savez_compressed('mnist_scaled.npz', X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
	'''

	mnist = np.load('mnist_scaled.npz')
	X_train, X_test, y_train, y_test = mnist['X_train'], mnist['X_test'], mnist['y_train'], mnist['y_test']
	from neuralnet import NeuralNetMLP
	nn = NeuralNetMLP(n_hidden=100, l2=0.01, epochs=200, eta=0.005, minibatch_size=100, shuffle=True, seed=1)
	nn.fit(X_train=X_train[:50000], y_train=y_train[:50000], X_valid=X_train[50000:], y_valid=y_train[50000:])

	fig = plt.figure()
	plt.plot(range(nn.epochs), nn.eval_['cost'])
	plt.ylabel('Cost')
	plt.xlabel('Epochs')
	fig.savefig('NeuralNetMLP_cost.pdf')

	fig = plt.figure()
	plt.plot(range(nn.epochs), nn.eval_['train_acc'], label='training')
	plt.plot(range(nn.epochs), nn.eval_['valid_acc'], label='validation', linestyle='--')
	plt.ylabel('Accuracy')
	plt.xlabel('Epochs')
	fig.savefig('NeuralNetMLP_acc.pdf')


	y_test_pred = nn.predict(X_test)
	acc = (np.sum(y_test == y_test_pred).astype(np.float)/X_test.shape[0])
	print('Training accuracy: %.2f%%' % (acc*100))
	miscl_img = X_test[y_test != y_test_pred][:25]
	correct_lab = y_test[y_test != y_test_pred][:25]
	miscl_lab = y_test_pred[y_test != y_test_pred][:25]
	fig, ax =plt.subplots(nrows=5, ncols=5, sharex=True, sharey=True)
	ax = ax.flatten()
	for i in range(25):
		img = miscl_img[i].reshape(28,28)
		ax[i].imshow(img, cmap='Greys', interpolation='nearest')
		ax[i].set_title('%d) t: %d p: %d' % (i+1, correct_lab[i], miscl_lab[i]))
	ax[0].set_xticks([])
	ax[0].set_yticks([])
	plt.tight_layout()
	fig.savefig('NeuralNetMLP_miscl.pdf')
