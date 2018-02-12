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

def load_mnist(path, kind='train'):
	'''Load MNIST data from path'''
	labels_path = os.path.join(path, '%s-labels-idx1-ubyte' % kind)
	images_path = os.path.join(path, '%s-images-idx3-ubyte' % kind)
	with open(labels_path, 'rb') as lbpath:
		magic, n = struct.unpack('>II', lbpath.read(8))
		labels = np.fromfile(lbpath, dtype=np.uint8)
	with open(images_path, 'rb') as imgpath:
		magic, num, rows, cols = struct.unpack('>IIIII', imgpath.read(16))
		images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
		images = ((images/255)-0.5)*2
	return images, labels

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

	np.savez_compressed('mnist_scaled.npz', X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
	'''
	mnist = np.load('mnist_scaled.npz')

