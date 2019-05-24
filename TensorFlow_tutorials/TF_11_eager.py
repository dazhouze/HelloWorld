#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
https://www.tensorflow.org/tutorials/eager/eager_basics
'''
# modules for pdf plot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns
# modules for TensorFlow
import tensorflow as tf
from tensorflow import keras
import numpy as np

def main():
	tf.enable_eager_execution()
	print(tf.add(1, 2))  # 1+2
	print(tf.add([1, 2], [3, 4])) # [] + []
	print(tf.square(5))  # 5**2
	print(tf.reduce_sum([1, 2, 3]))
	print(tf.encode_base64("hello world"))
	print(tf.square(2) + tf.square(3))
	
	x = tf.random_uniform([3, 3])
	print("Is there a GPU available: "),
	print(tf.test.is_gpu_available())
	print("Is the Tensor on GPU #0:  "),
	print(x.device.endswith('GPU:0'))
	
	# Force execution on CPU
	print("On CPU:")
	with tf.device("CPU:0"):
		x = tf.random_uniform([1000, 1000])
		assert x.device.endswith("CPU:0")
	
	# Force execution on GPU #0 if available
	if tf.test.is_gpu_available():
		with tf.device("GPU:0"): # Or GPU:1 for the 2nd GPU, GPU:2 for the 3rd etc.
			x = tf.random_uniform([1000, 1000])
			assert x.device.endswith("GPU:0")
	
if __name__ == '__main__':
	print('TensorFlow version', tf.__version__)
	print('Keras version', keras.__version__)
	main()
