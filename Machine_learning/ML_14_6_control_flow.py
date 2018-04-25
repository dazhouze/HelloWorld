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
	# python control flow
	x, y = 1., 2.
	g = tf.Graph()
	with g.as_default():
		tf_x = tf.placeholder(dtype=tf.float32, shape=None, name='tf_x')
		tf_y = tf.placeholder(dtype=tf.float32, shape=None, name='tf_y')
		if x < y:
			res = tf.add(tf_x, tf_y, name='result_add')
		else:
			res = tf.subtract(tf_x, tf_y, name='result_sub')
		print('Object', res)
	with tf.Session(graph=g) as sess:
		print('x<y: %s -> Result:' % (x<y), res.eval(feed_dict={'tf_x:0': x, 'tf_y:0': y}))
		x, y = 2., 1.
		print('x<y: %s -> Result:' % (x<y), res.eval(feed_dict={'tf_x:0': x, 'tf_y:0': y}))

	# tensorflow control flow
	x, y = 1., 2.
	g = tf.Graph()
	with g.as_default():
		tf_x = tf.placeholder(dtype=tf.float32, shape=None, name='tf_x')
		tf_y = tf.placeholder(dtype=tf.float32, shape=None, name='tf_y')
		res = tf.cond(tf_x < tf_y, lambda: tf.add(tf_x, tf_y, name='result_add'), lambda: tf.subtract(tf_x, tf_y, name='result_sub'))
		print('Object:', res)
	with tf.Session(graph=g) as sess:
		print('x<y: %s -> Result:' % (x < y), res.eval(feed_dict={'tf_x:0': x, 'tf_y:0': y}))
		x, y = 2., 1.
		print('x<y: %s -> Result:' % (x < y), res.eval(feed_dict={'tf_x:0': x, 'tf_y:0': y}))
