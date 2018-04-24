#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


if __name__ == '__main__':
	g = tf.Graph()
	# define the computation graph
	with g.as_default():
		# define tensors t1 t2 t3
		t1 = tf.constant(np.pi)
		t2 = tf.constant([1 ,2 , 3, 4])
		t3 = tf.constant([[1, 2], [3, 4]])
		# get their ranks
		r1 = tf.rank(t1)
		r2 = tf.rank(t2)
		r3 = tf.rank(t3)
		# get their shapes
		s1 = t1.get_shape()
		s2 = t2.get_shape()
		s3 = t3.get_shape()
		print('Shapes',  s1, s2, s3)
	with tf.Session(graph=g) as sess:
		print('Ranks:', r1.eval(), r2.eval(), r3.eval())

	g = tf.Graph()
	with g.as_default():
		a = tf.constant(1, name='a')
		b = tf.constant(2, name='b')
		c = tf.constant(3, name='c')
		z = 2*(a-b) + c
	with tf.Session(graph=g) as sess:
		print('2*(a-b) + c:', sess.run(z))

	g = tf.Graph()
	with g.as_default():
		tf_a = tf.placeholder(tf.int32, shape=[], name='tf_a')  # placeholder
		tf_b = tf.placeholder(tf.int32, shape=[], name='tf_b')  # placeholder
		tf_c = tf.placeholder(tf.int32, shape=[], name='tf_c')  # placeholder
		r1 = tf_a - tf_b  # intermediate result tensors
		r2 = 2*r1
		z = r2 + tf_c  # tnsor of the final result
	with tf.Session(graph=g) as sess:
		feed = {tf_a: 1, tf_b: 2, tf_c: 3}
		print('z:', sess.run(z, feed_dict=feed))

	g = tf.Graph()
	with g.as_default():
		tf_x = tf.placeholder(tf.float32, shape=[None, 2], name='tf_x')
		x_mean = tf.reduce_mean(tf_x, axis=0, name='mean')
	np.random.seed(123)
	np.set_printoptions(precision=2)
	with tf.Session(graph=g) as sess:
		x1 = np.random.uniform(low=0, high=1, size=(5, 2))
		print('Feeding data with shape ', x1.shape)
		print('Result:', sess.run(x_mean, feed_dict={tf_x: x1}))
		x2 = np.random.uniform(low=0, high=1, size=(10,2))
		print('Feeding data with shape', x2.shape)
		print('Result:', sess.run(x_mean, feed_dict={tf_x: x2}))

	g1 = tf.Graph()
	with g1.as_default():
		w = tf.Variable(np.array([[1,2,3,4], [5,6,7,8]]), name='w')
		print(w)

	g2 = tf.Graph()
	with g2.as_default():
		w1 = tf.Variable(1, name='w1')
		init_op = tf.global_variables_initializer()
		w2 = tf.Variable(2, name='w2')
	with tf.Session(graph=g2) as sess:
		sess.run(init_op)
		print('w1:', sess.run(w1))
