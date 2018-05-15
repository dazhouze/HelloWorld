#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import pandas as pd
import numpy as np
import tensorflow as tf
import keras

def vectorize_sequences(sequences, dimension=10000):
	results = np.zeros((len(sequences), dimension))
	for i, sequence in enumerate(sequences):
		results[i, sequence] = 1.
	return results

def to_one_hot(labels, dimension=46):
	results = np.zeros((len(labels), dimension))
	for i, label in enumerate(labels):
		results[i, label] = 1.
	return results

if __name__ == '__main__':
	from keras.datasets import reuters
	(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)
	word_index = reuters.get_word_index()
	reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
	decoded_newswire = ' '.join([reverse_word_index.get(i-3, '?') for i in train_data[0]])
	print(decoded_newswire)

	x_train = vectorize_sequences(train_data)
	x_test = vectorize_sequences(test_data)
	one_hot_train_labels = to_one_hot(train_labels)
	one_hot_test_labels = to_one_hot(test_labels)
	from keras.utils.np_utils import to_categorical
	one_hot_train_labels = to_categorical(train_labels)
	one_hot_test_labels = to_categorical(test_labels)

	from keras import models
	from keras import layers
	model = models.Sequential()
	model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(46, activation='softmax'))
	model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
	x_val = x_train[:1000]
	partial_x_train = x_train[1000:]
	y_val = one_hot_train_labels[:1000]
	partial_y_train = one_hot_train_labels[1000:]

	history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))
	model.save('./DL_3_5.h5')
	results = model.evaluate(x_test, one_hot_test_labels)
	print(results)


	with matplotlib.backends.backend_pdf.PdfPages('DL_3_5.pdf') as pdf_all: 
		history_dict = history.history
		print(history_dict.keys())
		loss_values = history_dict['loss']
		val_loss_values = history_dict['val_loss']
		epochs = range(1, len(history_dict['acc'])+1)

		fig = plt.figure()
		plt.plot(epochs, loss_values, 'bo', label='Training loss')  # blue dot
		plt.plot(epochs, val_loss_values, 'b', label='Training loss')  # blue line
		plt.title('Training and validation loss', fontsize=20)
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Loss', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)

		acc_values = history_dict['acc']
		val_acc_values = history_dict['val_acc']
		fig = plt.figure()
		plt.plot(epochs, acc_values, 'bo', label='Training acc')  # blue dot
		plt.plot(epochs, val_acc_values, 'b', label='Training acc')  # blue line
		plt.title('Training and validation loss', fontsize=20)
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Loss', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)


