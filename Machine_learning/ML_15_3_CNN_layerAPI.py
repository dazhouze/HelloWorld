#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import os

class ConvNN(object):
	def __init__(self, batchsize=64, epochs=20, learning_rate=1e-4, dropout_rate=0.5, shuffle=True, random_seed=None):
		np.random.seed(random_seed)
		self.__batchsize = batchsize
		self.__epochs = epochs
		self.__learning_rate = learning_rate
		self.__dropout_rate = dropout_rate
		self.__shuffle = shuffle

		g = tf.Graph()
		with g.as_default():
			tf.set_random_seed(random_seed)  # set random seed
			self.build()  # build the network
			self.init_op = tf.global_variables_initializer()  # initializer
			self.saver = tf.train.Saver()  # saver
		self.sess = tf.Session(graph=g)  # creat a session

	def build(self):
		# placeholder for X and y
		tf_x = tf.placeholder(tf.float32, shape=[None, 784], name='tf_x')
		tf_y = tf.placeholder(tf.int32, shape=[None], name='tf_y')
		is_train = tf.placeholder(tf.bool, shape=(), name='is_train')
		# reshape x to a 4D tensor [batchsize, width, height, 1]
		tf_x_image = tf.reshape(tf_x, shape=[-1, 28, 28, 1], name='input_x_2dimages')
		tf_y_onehot = tf.one_hot(indices=tf_y, depth=10, dtype=tf.float32, name='input_y_onthot')
		# 1st layer: Conv_1
		h1 = tf.layers.conv2d(tf_x_image, kernel_size=(5, 5), filters=32, activation=tf.nn.relu)
		# MaxPooling
		h1_pool = tf.layers.max_pooling2d(h1, pool_size=(2,2), strides=(2,2))
		# 2nd layer: Conv_2
		h2 = tf.layers.conv2d(h1_pool, kernel_size=(5, 5), filters=64, activation=tf.nn.relu)
		# MacPooling
		h2_pool = tf.layers.max_pooling2d(h2, pool_size=(2, 2), strides=(2, 2))
		# 3rd layer: Fully Connected
		input_shape = h2_pool.get_shape().as_list()
		n_input_units = np.prod(input_shape[1:])
		h2_pool_flat = tf.reshape(h2_pool, shape=[-1, n_input_units])
		h3 = tf.layers.dense(h2_pool_flat, 1024, activation=tf.nn.relu)
		# Dropout
		h3_drop = tf.layers.dropout(h3, rate=self.__dropout_rate, training=is_train)
		# 4th layer: Fully Connected (linear activation)
		h4 = tf.layers.dense(h3_drop, 10, activation=None)
		# Prediction
		predictions = {'probabilities': tf.nn.softmax(h4, name='probabilities'), 'labels': tf.cast(tf.argmax(h4, axis=1), tf.int32, name='labels')}
		# Loss Funcion and Optimization
		cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=h4, labels=tf_y_onehot), name='cross_entropy_loss')
		# Optimizer:
		optimizer = tf.train.AdamOptimizer(self.__learning_rate)
		optimizer = optimizer.minimize(cross_entropy_loss, name='train_op')
		# Finding accuracy
		correct_predictions = tf.equal(predictions['labels'], tf_y, name='correct_preds')
		accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32), name='accuracy')

	def save(self, epoch, path='./tflayers-model/'):
		if not os.path.isdir(path):
			os.makedirs(path)
		print('Saving model in %s' % path)
		self.saver.save(self.sess, os.path.join(path, 'model.ckpt'), global_step=epoch)

	def load(self, epoch, path):
		print('Loading model from %s' % path)
		self.saver.restore(self.sess, os.path.join(path, 'model.ckpt-%d' % epoch))

	def train(self, training_set, validation_set=None, initialize=True):
		# initialize variables
		if initialize:
			self.sess.run(self.init_op)
		self.__train_cost_ = []
		X_data, y_data = np.array(training_set[0]), np.array(training_set[1])
		for epoch in range(1, self.__epochs+1):
			batch_gen = batch_generator(X_data, y_data, shuffle=self.__shuffle)
			avg_loss = 0.
			for i, (batch_x, batch_y) in enumerate(batch_gen):
				feed = {'tf_x:0': batch_x, 'tf_y:0': batch_y, 'is_train:0': True}  # for dropout
				loss, _  = self.sess.run(['cross_entropy_loss:0', 'train_op'], feed_dict=feed)
				avg_loss += loss
			print('Epoch %02d: Training Avg. Loss: %7.3f' % (epoch, avg_loss), end=' ')
			if validation_set is not None:
				feed = {'tf_x:0': batch_x, 'tf_y:0': batch_y, 'is_train:0': False}  # for dropout
				valid_acc = self.sess.run('accuracy:0', feed_dict=feed)
				print('Validation Acc: %7.3f' % valid_acc)
			else:
				print()
	
	def predict(self, X_test, return_proba=False):
		feed = {'tf_x:0': X_test, 'is_train:0': False}  # for dropout
		if return_proba:
			return self.sess.run('probabilities:0', feed_dict=feed)
		else:
			return self.sess.run('labels:0', feed_dict=feed)

def batch_generator(X, y, batch_size=64, shuffle=False, random_seed=None):
	idx = np.arange(y.shape[0])
	if shuffle:
		rng = np.random.RandomState(random_seed)
		rng.shuffle(idx)
		X = X[idx]
		y = y[idx]
	for i in range(0, X.shape[0], batch_size):
		yield (X[i:i+batch_size, :], y[i:i+batch_size])

if __name__ == '__main__':

	mnist = np.load('mnist_scaled.npz')
	X_train_tem, X_test, y_train_tem, y_test = mnist['X_train'], mnist['X_test'], mnist['y_train'], mnist['y_test']
	X_train=X_train_tem[:50000]
	y_train=y_train_tem[:50000]
	X_valid=X_train_tem[50000:]
	y_valid=y_train_tem[50000:]
	mean_vals = np.mean(X_train, axis=0)
	std_val = np.std(X_train)
	X_train_centered = (X_train - mean_vals)/std_val
	X_valid_centered = (X_valid - mean_vals)/std_val
	X_test_centered = (X_test - mean_vals)/std_val

	cnn = ConvNN(random_seed=123)
	cnn.train(training_set=(X_train_centered, y_train), validation_set=(X_valid_centered, y_valid), initialize=True)
	cnn.save(epoch=20)
	del cnn

	cnn2 = ConvNN(random_seed=123)
	cnn2.load(epoch=20, path='./tflayers-model/')
	print(cnn2.predict(X_test_centered[:10, :]))
	
	preds = cnn2.predict(X_test_centered)
	print('Test Accuracy %.2f%%' % (100*np.sum(y_test == preds)/len(y_test)))

	
