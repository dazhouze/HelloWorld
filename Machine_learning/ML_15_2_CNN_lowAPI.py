#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
import tensorflow as tf
import scipy.misc
import os

def batch_generator(X, y, batch_size=64, shuffle=False, random_seed=None):
	idx = np.arange(y.shape[0])
	if shuffle:
		rng = np.random.RandomState(random_seed)
		rng.shuffle(idx)
		X = X[idx]
		y = y[idx]
	for i in range(0, X.shape[0], batch_size):
		yield (X[i:i+batch_size, :], y[i:i+batch_size])

def conv_layer(input_tensor, name, kernel_size, n_output_channels, padding_mode='SAME', strides=(1,1,1,1)):
	with tf.variable_scope(name):
		# get n_input_channels:
		# input tensor shape:
		# [batch * width * height * channels_in]
		input_shape = input_tensor.get_shape().as_list()
		n_input_channels = input_shape[-1]
		weights_shape = list(kernel_size) + [n_input_channels, n_output_channels]
		weights = tf.get_variable(name='_weights', shape=weights_shape)
		print(weights)
		biases = tf.get_variable(name='_biases', initializer=tf.zeros(shape=[n_output_channels]))
		print(biases)
		conv = tf.nn.conv2d(input=input_tensor, filter=weights, strides=strides, padding=padding_mode)
		print(conv)
		conv = tf.nn.bias_add(conv, biases, name='net_pre-activation')
		print(conv)
		conv = tf.nn.relu(conv, name='activation')
		print(conv)
		return conv

def fc_layer(input_tensor, name, n_output_units, activation_fn=None):
	with tf.variable_scope(name):
		input_shape = input_tensor.get_shape().as_list()[1:]
		n_input_unites = np.prod(input_shape)
		if len(input_shape) > 1:
			input_tensor = tf.reshape(input_tensor, shape=(-1, n_input_unites))
		weights_shape = [n_input_unites, n_output_units]
		weights = tf.get_variable(name='_weights', shape=weights_shape)
		print(weights)
		biases = tf.get_variable(name='_biases', initializer=tf.zeros(shape=[n_output_units]))
		print(biases)
		layer = tf.matmul(input_tensor, weights)
		print(layer)
		layer = tf.nn.bias_add(layer, biases, name='net_pre-activation')
		print(layer)
		if activation_fn is None:
			return layer
		layer = activation_fn(layer, name='activation')
		print(layer)
		return(layer)

def build_cnn():
	# placeholder for X and y:
	tf_x = tf.placeholder(tf.float32, shape=[None, 784], name='tf_x')
	tf_y = tf.placeholder(tf.int32, shape=[None], name='tf_y')
	#reshpae x to a 4D tensor: [batchsize, width, hight, 1]
	tf_x_image = tf.reshape(tf_x, shape=[-1, 28, 28, 1], name='tf_x_reshaped')
	# ont-hot enconding
	tf_y_onehot = tf.one_hot(indices=tf_y, depth=10, dtype=tf.float32, name='tf_y_onthot')
	# 1st layer: Conv_1
	print('\nBuilding 1st layer:')
	h1 = conv_layer(tf_x_image, name='conv_1', kernel_size=(5,5), padding_mode='VALID', n_output_channels=32)
	# MaxPooling
	h1_pool = tf.nn.max_pool(h1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
	# 2nd layer: Conv_2
	print('\n Buliding 2nd layer:')
	h2 = conv_layer(h1_pool, name='conv_2', kernel_size=(5,5), padding_mode='VALID', n_output_channels=64)
	# MaxPooling
	h2_pool = tf.nn.max_pool(h2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
	# 3rd layer: FullyCnnected
	print('\nBuliding 3rd layer:')
	h3 = fc_layer(h2_pool, name='fc_3', n_output_units=1024, activation_fn=tf.nn.relu)
	# Dropout
	keep_prob = tf.placeholder(tf.float32, name='fc_keep_prob')
	h3_drop = tf.nn.dropout(h3, keep_prob=keep_prob, name='dropout_layer')
	# 4th layer: Fully Cnnected(linerar activation)
	print('\nBuilding 4th layer:')
	h4 = fc_layer(h3_drop, name='fc-4', n_output_units=10, activation_fn=None)
	# Prdiction
	predictions = {'probabilities': tf.nn.softmax(h4, name='probabilities'), 'labels': tf.cast(tf.argmax(h4, axis=1), tf.int32, name='labels')}
	# Visualize the graph with TensorBoard:
	# Loss Function and Optimization
	cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=h4, labels=tf_y_onehot), name='cross_entropy_loss')
	# Optimizer:
	optimizer = tf.train.AdamOptimizer(learning_rate)
	opetimizer = optimizer.minimize(cross_entropy_loss, name='train_op')
	# Computing the prediction accuracy
	correct_predictions = tf.equal(predictions['labels'], tf_y, name='crrect_preds')
	accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32), name='accuracy')

def save(szver, sess, epoch, path='./model/'):
	if not os.path.isdir(path):
		os.makedirs(path)
	print('Saving model in %s' % path)
	saver.save(sess, os.path.join(path, 'cnn-model.ckpt'), global_step=epoch)

def load(saver, sess, path, epoch):
	print('Loding model from %s' % path)
	saver.restore(sess, os.path.join(path, 'cnn-model.ckpt-%d' % epoch))

def train(sess, training_set, validation_set=None, initialize=True, epochs=20, shuffle=True, dropout=0.5, random_seed=None):
	X_data = np.array(training_set[0])
	y_data = np.array(training_set[1])
	training_loss = []
	# initialize variables
	if initialize:
		sess.run(tf.global_variables_initializer())
	np.random.seed(random_seed)  # for shuflling in bathc generator
	for epoch in range(1, epochs+1):
		batch_gen = batch_generator(X_data, y_data, shuffle=shuffle)
		avg_loss = 0.0
		for i,(batch_x,batch_y) in enumerate(batch_gen):
			feed = {'tf_x:0': batch_x, 'tf_y:0': batch_y, 'fc_keep_prob:0': dropout}
			loss, _ = sess.run(['cross_entropy_loss:0', 'train_op'], feed_dict=feed)
			avg_loss += loss
		
		training_loss.append(avg_loss/(i+1))
		print('Epoch %02d Training Avg. Loss: %7.3f' % (epoch, avg_loss), end=' ')
		if validation_set is not None:
			feed = {'tf_x:0': validation_set[0], 'tf_y:0': validation_set[1], 'fc_keep_prob:0': 1.0}
			valid_acc = sess.run('accuracy:0', feed_dict=feed)
			print(' Validation Acc: %7.3f' % valid_acc)
		else:
			print()

def predict(sess, X_test, return_proba=False):
	feed = {'tf_x:0': X_test, 'fc_keep_prob:0': 1.0}
	if return_proba:
		return sess.run('probabilities:0', feed_dict=feed)
	else:
		return sess.run('labels:0', feed_dict=feed)

if __name__ == '__main__':
	img = scipy.misc.imread('example-image.png', mode='RGB')
	print('Image shape:', img.shape)
	print('Number of channels:', img.shape[2])
	print('Image data type:', img.dtype)
	print(img[100:102, 100:102, :])
	

	mnist = np.load('mnist_scaled.npz')
	X_train, X_test, y_train, y_test = mnist['X_train'], mnist['X_test'], mnist['y_train'], mnist['y_test']
	X_train=X_train[:45000]
	y_train=y_train[:45000]
	X_valid=X_train[45000:]
	y_valid=y_train[45000:]
	mean_vals = np.mean(X_train, axis=0)
	std_val = np.std(X_train)
	X_train_centered = (X_train - mean_vals)/std_val
	X_valid_centered = (X_valid - mean_vals)/std_val
	X_test_centered = (X_test - mean_vals)/std_val
	
	# test conv_layer
	g = tf.Graph()
	with g.as_default():
		x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
		conv_layer(x, name='convtest', kernel_size=(3,3), n_output_channels=32)
	del g, x

	# test fc_layer
	g = tf.Graph()
	with g.as_default():
		x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
		fc_layer(x, name='fctest', n_output_units=32, activation_fn=tf.nn.relu)
	del g, x

	# Define hyperparaneters
	learning_rate=1e-4
	random_seed = 123

	# create a graph
	g =tf.Graph()
	with g.as_default():
		tf.set_random_seed(random_seed)
		# bulid the graph
		build_cnn()
		# saver:
		saver = tf.train.Saver()
	# create a TF session and train the CNN model
	with tf.Session(graph=g) as sess:
		train(sess, training_set=(X_train_centered, y_train), validation_set=(X_valid_centered, y_valid), initialize=True, random_seed=123)
		save(saver, sess, epoch=20)
	del g

	# calculate prediction accuracy on the test set restoring the saved model
	g2 = tf.Graph()
	with g2.as_default():
		tf.set_random_seed(random_seed)
		build_cnn()
		saver =tf.train.Saver()
	# creat a new session and restroe the model
	with tf.Session(graph=g2) as sess:
		load(saver, sess, epoch=20, path='./model/')
		preds = predict(sess, X_test_centered, return_proba=False)
		print('Test Accuracy: %.3f%%' % (100*np.sum(preds == y_test)/len(y_test)))

	# continue training for 20 more epochs without reinitializing :: intialize=False
	with tf.Session(graph=g2) as sess:
		load(saver, sess, epoch=20, path='./model/')
		train(sess, training_set=(X_train_centered, y_train), validation_set=(X_valid_centered, y_valid), initialize=False, epochs=20, random_seed=123)
		save(saver, sess, epoch=40, path='./model/')
		preds = predict(sess, X_test_centered, return_proba=False)
		print('Test Accuracy: %.3f%%' % (100*np.sum(preds == y_test)/len(y_test)))
