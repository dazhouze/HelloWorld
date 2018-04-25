#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
import tensorflow as tf


if __name__ == '__main__':
	g = tf.Graph()
	with g.as_default():
		with tf.variable_scope('net_A'):
			with tf.variable_scope('layer-1'):
				w1 = tf.Variable(tf.random_normal(shape=(10,4)), name='weights')
			with tf.variable_scope('layer-2'):
				w2 = tf.Variable(tf.random_normal(shape=(20,10)), name='weights')
		with tf.variable_scope('net_B'):
			with tf.variable_scope('layer-1'):
				w3 = tf.Variable(tf.random_normal(shape=(10,4)), name='weights')
		print(w1)
		print(w2)
		print(w3)
