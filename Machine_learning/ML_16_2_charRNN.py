#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tensorflow as tf
import pyprind
from string import punctuation
import re
import os
from collections import Counter
np.random.seed(123)

class CharRNN(object):
	def __init__(self, num_classes, batch_size=64, num_steps=100, lstm_size=128, num_layers=1, learning_rate=0.001, keep_prob=0.5, grad_clip=5, sampling=False):
		self.__num_classes = num_classes
		self.__batch_size = batch_size
		self.__num_steps = num_steps
		self.__lstm_size = lstm_size
		self.__num_layers = num_layers
		self.__learning_rate = learning_rate
		self.__keep_prob = keep_prob
		self.__grad_clip = grad_clip
		self.__g = tf.Graph()
		with self.__g.as_default():
			tf.set_random_seed(123)
			self.build(sampling=sampling)
			self.saver = tf.train.Saver()
			self.init_op = tf.global_variables_initializer()

	def build(self, sampling):
		if sampling == True:
			batch_size, num_steps = 1, 1
		else:
			batch_size = self.__batch_size
			num_steps = self.__num_steps
		tf_x = tf.placeholder(tf.int32, shape=[batch_size, num_steps], name='tf_x')
		tf_y = tf.placeholder(tf.int32, shape=[batch_size, num_steps], name='tf_y')
		tf_keepprob = tf.placeholder(tf.float32, name='tf_keepprob')
		# one-hot encoding:
		x_onehot = tf.one_hot(tf_x, depth=self.__num_classes)
		y_onehot = tf.one_hot(tf_y, depth=self.__num_classes)
		# build the multi-layer RNN cells
		cells = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.DropoutWrapper(tf.contrib.rnn.BasicLSTMCell(self.__lstm_size), output_keep_prob=tf_keepprob) for _ in range(self.__num_layers)])
		# Define the initial state
		self.__initial_state = cells.zero_state(batch_size, tf.float32)
		# Run each sequence step through the RNN
		lstm_outputs, self.__final_state =  tf.nn.dynamic_rnn(cells, x_onehot, initial_state = self.__initial_state)
		print(' << lstm_outputs >>', lstm_outputs)
		seq_output_reshaped = tf.reshape(lstm_outputs, shape=[-1, self.__lstm_size], name='seq_output_reshaped')
		logits = tf.layers.dense(inputs=seq_output_reshaped, units=self.__num_classes, activation=None, name='logits')
		proba = tf.nn.softmax(logits, name='probabilities')
		y_reshaped = tf.reshape(y_onehot, shape=[-1, self.__num_classes], name='y_reshaped')
		cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y_reshaped), name='cost')
		# Gradient clipping to avoid 'exploding gradients'
		tvars = tf.trainable_variables()
		grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), self.__grad_clip)
		optimizer = tf.train.AdamOptimizer(self.__learning_rate)
		train_op = optimizer.apply_gradients(zip(grads, tvars), name='train_op')
		
	def train(self, X_train, y_train, num_epochs, ckpt_dir='./model/'):
		# create the checkpoint directory
		if not os.path.exists(ckpt_dir):
			os.mkdir(ckpt_dir)
		with tf.Session(graph=self.__g) as sess:
			sess.run(self.init_op)
			n_batches = int(train_x.shape[1]/self.__num_steps)
			iterations = n_batches * num_epochs
			for epoch in range(num_epochs):
				# Train network
				new_state = sess.run(self.__initial_state)
				loss = 0
				# Mini-batch generator:
				bgen = create_batch_generator(train_x, train_y, self.__num_steps)
				for b, (batch_x, batch_y) in enumerate(bgen, 1):
					iteration = epoch*n_batches + b
					feed = {'tf_x:0': batch_x, 'tf_y:0': batch_y, 'tf_keepprob:0': self.__keep_prob, self.__initial_state: new_state}
					batch_cost, _, new_state = sess.run(['cost:0', 'train_op', self.__final_state], feed_dict=feed)
				if iteration % 10 == 0:
					print('Epoch %d/%d Iteration %d' '| Training loss: %.4f' % (epoch+1, num_epochs, iteration, batch_cost))
			# Save the trained model
			self.saver.save(sess, os.path.join(ckpt_dir, 'language_modeling.ckpt'))

	def sample(self, output_length, ckpt_dir, starter_seq='The '):
		observed_seq = [ch for ch in starter_seq]
		with tf.Session(graph=self.__g) as sess:
			self.saver.restore(sess, tf.train.latest_checkpoint(ckpt_dir))
			# 1: run the model using the starter sequence
			new_state = sess.run(self.__initial_state)
			for ch in starter_seq:
				x = np.zeros((1, 1))
				x[0, 0] = char2int[ch]
				feed = {'tf_x:0': x, 'tf_keepprob:0': 1.0, self.__initial_state: new_state}
				proba, new_state = sess.run(['probabilities:0', self.__final_state], feed_dict=feed)
			ch_id = get_top_char(proba, len(chars))
			observed_seq.append(int2char[ch_id])
			# 2: run the model using the updated observed_seq
			for i in range(output_length):
				x[0, 0] = ch_id
				feed = {'tf_x:0': x, 'tf_keepprob:0':1., self.__initial_state: new_state}
				proba, new_state = sess.run(['probabilities:0', self.__final_state], feed_dict=feed)
				ch_id = get_top_char(proba, len(chars))
				observed_seq.append(int2char[ch_id])
		return ''.join(observed_seq)
	
	def predict(self, X_data, return_proba=False):
		preds = []
		with tf.Session(graph = self.__g) as sess:
			self.saver.restore(sess, tf.train.latest_checkpoint('./model/'))
			test_state = sess.run(self.__initial_state)
			for ii, batch_x in enumerate(create_batch_generator(X_data, None, batch_size=self.__batch_size), 1):
				feed = {'tf_x:0': batch_x, 'tf_keepprob:0': 1.0, self.__initial_state: test_state}
				if return_proba:
					pred, test_state = sess.run(['probabilities:0', self.__final_state], feed_dict=feed)
				else:
					pred, test_state = sess.run(['labels:0', self.__final_state], feed_dict=feed)
				preds.append(pred)
		return np.concatenate(preds)

def reshape_data(sequence, batch_size, num_steps):
	tot_batch_length = batch_size * num_steps
	num_batches = int(len(sequence)/tot_batch_length)
	if num_batches*tot_batch_length + 1 > len(sequence):
		num_batches = num_batches - 1
	# Truncate the sequence at the end to get rid of remaining charcaters that do not make a full batch
	x = sequence[0: num_batches*tot_batch_length]
	y = sequence[1: num_batches*tot_batch_length + 1]
	# Split x & y into a list batches of sequences:
	x_batch_splits = np.split(x, batch_size)
	y_batch_splits = np.split(y, batch_size)
	# Stack the batches together batch_size * tot_batch_length
	x = np.stack(x_batch_splits)
	y = np.stack(y_batch_splits)
	return x, y

def create_batch_generator(data_x, data_y, num_steps):
	batch_size, tot_batch_length = data_x.shape
	num_batches = int(tot_batch_length/num_steps)
	for b in range(num_batches):
		yield (data_x[:, b*num_steps:(b+1)*num_steps], data_y[:, b*num_steps:(b+1)*num_steps])

def get_top_char(probas, char_size, top_n=5):
	p = np.squeeze(probas)
	p[np.argsort(p)[:-top_n]] = 0.
	p = p/np.sum(p)
	ch_id = np.random.choice(char_size, 1, p=p)[0]
	return ch_id

if __name__ == '__main__':
	# preparing the data
	with open('pg2265.txt', 'r', encoding='utf-8') as f:
		text = f.read()
	text = text[15858:]
	chars = set(text)
	char2int = {ch:1 for i,ch in enumerate(chars)}
	int2char = dict(enumerate(chars))
	text_ints = np.array([char2int[ch] for ch in text], dtype=np.int32)

	batch_size = 64
	num_steps = 100
	train_x, train_y = reshape_data(text_ints, batch_size, num_steps)
	rnn = CharRNN(num_classes=len(chars), batch_size=batch_size)
	rnn.train(train_x, train_y, num_epochs=100, ckpt_dir='./model-100/')
	
	del rnn
	np.random.seed(123)
	rnn = CharRNN(len(chars), sampling=True)
	print(rnn.sample(ckpt_dir='./model-100/', output_length=500))
