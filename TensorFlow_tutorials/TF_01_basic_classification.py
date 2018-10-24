#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
https://www.tensorflow.org/tutorials/keras/basic_classification
'''

import tensorflow as tf
from tensorflow import keras
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

def MNIST():
	# Fashion MNIST dataset which contains 70,000 grayscale images in 10 categories
	fashion_mnist = keras.datasets.fashion_mnist
	(train_images, trian_labels), (test_images, test_labels) = fashion_mnist.load_data()


if __name__ == '__main__':
	print('TensorFlow version', tf.__version__)
	print('Keras version', keras.__version__)
	MNIST()

