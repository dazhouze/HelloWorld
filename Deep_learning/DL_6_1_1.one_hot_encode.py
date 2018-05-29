#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import tensorflow as tf
import keras

if __name__ == '__main__':
	# word level one hot encoding
	samples = ['The cat sat on the mat.', 'The dog ate my homework.']
	token_index = {}
	for sample in samples:
		for word in sample.split():
			if word not in token_index:
				token_index[word] = len(token_index) + 1
	max_length = 10
	results = np.zeros(shape=(len(samples), max_length, max(token_index.values()) + 1))
	for i, sample in enumerate(samples):
		for j, word in list(enumerate(sample.split()))[:max_length]:
			index = token_index.get(word)
			results[i, j, index] = 1.
	print(results)

	# character level one hot encoding
	import string
	samples = ['The cat sat on the mat.', 'The dog ate my homework.']
	characters = string.printable
	token_index = dict(zip(range(1, len(characters) + 1), characters))
	max_length = 50
	results = np.zeros((len(samples), max_length, max(token_index.keys()) + 1))
	for i, sample in enumerate(samples):
		for j, character in enumerate(sample):
			index = token_index.get(character)
			results[i, j, index] = 1.
	print(results)

	# keras for word level one-hot enconding
	from keras.preprocessing.text import Tokenizer
	samples = ['The cat sat on the mat.', 'The dog ate my homework.']
	tokenizer = Tokenizer(num_words=1000)
	tokenizer.fit_on_texts(samples)

	sequences = tokenizer.texts_to_sequences(samples)
	one_hot_results = tokenizer.texts_to_matrix(samples, mode='binary')
	word_index = tokenizer.word_index

	print('Fountd %s uniques tokens.' % len(word_index))
	print(word_index, one_hot_results, sequences)

	# word level one-hot with hashing trick
	samples = ['The cat sat on the mat.', 'The dog ate my homework.']
	dimensionality = 1000
	max_length = 10
	results = np.zeros((len(samples), max_length, dimensionality))
	for i, sample in enumerate(samples):
		for j, word in list(enumerate(sample.split()))[:max_length]:
			index = abs(hash(word)) % dimensionality
			results[i, j, index] =1.
	print(results)
