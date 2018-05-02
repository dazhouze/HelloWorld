#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tensorflow as tf
import pyprind
from string import punctuation
import re
from collections import Counter
np.random.seed(123)

def creat_batch_generator(x, y=None, batch_size=64):
	n_batches = len(x)//batch_size
	x = x[:n_batches*batch_size]
	if y is not None:
		y = y[:n_batches*batch_size]
	for ii in range(0, len(x), batch_size):
		if y is not None:
			yield x[ii:ii+batch_size], y[ii:ii+batch_size]
		else:
			yield x[ii:ii+batch_size]

def SentimentRNN(object):
	def __init__(self, n_words, seq_len=200, lstm_size=256, num_layers=1, batch_size=64, learning_rate=0.0001, embed_size=200):
		self.n_words = n_words
		self.seq_len = seq_len
		self.lstm_size = lstm_size
		self.num_layers = num_layers
		self.batch_size = batch_size
		self.learning_size = learning_rate
		self.embed_size = embed_size
		self.g = tf.Graph()
		with self.g.as_default():
			tf.set_random_seed(123)
			self.build()
			self.saver = tf.train.Saver()
			self.init_op = tf.global_variables_initializer()

	def bulid(self):
        # Define the placeholders
        tf_x = tf.placeholder(tf.int32, shape=(self.batch_size, self.seq_len), name='tf_x')
        tf_y = tf.placeholder(tf.int32, shape=(self.batch_size, self.seq_len), name='tf_y')
        tf_keepprob = tf.placeholder(tf.float32, name='tf_keepprob')
        # creat the embedding layer

if __name__ == '__main__':
	# preparing the data
	df = pd.read_csv('movie_data.csv', encoding='utf-8')
	counts = Counter()
	pbar = pyprind.ProgBar(len(df['review']), title='Counting words occurrences')
	for i,review in enumerate(df['review']):
		text = ''.join([c if c not in punctuation else ' '+c+' ' for c in review]).lower()
		df.loc[i, 'review'] = text
		pbar.update()
		counts.update(text.split())

	# creat a mapping, Map each unique word to an integer
	word_counts = sorted(counts, key=counts.get, reverse=True)
	print(word_counts[:5])
	word_to_int = {word: ii for ii, word in enumerate(word_counts, 1)}
	mapped_reviews = []
	pdar = pyprind.ProgBar(len(df['review']), title='Map reviews to ints')
	for review in df['review']:
		mapped_reviews.append([word_to_int[word] for word in review.split()])
		pbar.update()

	# Define same-length sequences. if sequence length < 200: left-pad with zero. if > 200, last 200 only
	sequence_length = 200
	sequences = np.zeros((len(mapped_reviews), sequence_length), dtype=int)
	for i,row in enumerate(mapped_reviews):
		review_arr = np.array(row)
		sequences[i, -len(row):] = review_arr[-sequence_length:]
	X_train = sequences[:25000, :]
	y_train = df.loc[:25000, 'sentiment'].values
	X_test = sequences[25000:, :]
	y_test = df.loc[25000:, 'sentiment'].values

