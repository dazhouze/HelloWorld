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

def vctorize_sequences(sequences, dimension=10000):
	results = np.zeros((len(sequences), dimension))
	for i,sequence in enumerate(sequences):
		results[i, sequence] = 1.
	return results

if __name__ == '__main__':
	from keras.datasets import imdb
	# only keep top 10k most frequently occurring words
	(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
	word_index = imdb.get_word_index()
	reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
	decoded_review = ' '.join([reverse_word_index.get(i-3, '?') for i in train_data[0]])
	#print(decoded_review)
	print(train_data.shape, test_data.shape)
	
	x_train = vctorize_sequences(train_data)
	x_test = vctorize_sequences(test_data)
	y_train = np.asarray(train_labels).astype('float32')
	y_test = np.asarray(test_labels).astype('float32')
	x_val = x_train[:10000]  # validation set
	partial_x_train = x_train[10000:]
	y_val = y_train[:10000]
	partial_y_train = y_train[10000:]


	from keras import models
	from keras import layers
	model = models.Sequential()
	model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
	model.add(layers.Dense(16, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
	history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))
	results = model.evaluate(x_test, y_test)
	print('epochs=20', results)

	with matplotlib.backends.backend_pdf.PdfPages('DL_3_4.pdf') as pdf_all: 
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

	model = models.Sequential()
	model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
	model.add(layers.Dense(16, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
	history = model.fit(x_train, y_train, epochs=4, batch_size=512)
	results = model.evaluate(x_test, y_test)
	print('epochs=4', results)
	print(model.predict(x_test))  # genreate prdictions on new data

