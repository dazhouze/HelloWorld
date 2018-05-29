#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import keras

if __name__ == '__main__':
	from keras.datasets import imdb
	from keras.preprocessing import sequence
	max_features = 10000
	maxlen = 500
	batch_size = 32
	print('Loading data...')
	(input_train, y_train), (input_test, y_test) = imdb.load_data(num_words=max_features)
	print(len(input_train), 'train sequences')
	print(len(input_test), 'test sequences')
	print('Pad sequences (samples x time)')
	input_train = sequence.pad_sequences(input_train, maxlen=maxlen)
	input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
	print('input_train shape', input_train.shape)
	print('input_test shape', input_test.shape)

	from keras.layers import Embedding, Conv1D, MaxPooling1D, GRU, Dense
	from keras.models import Sequential
	from keras.optimizers import RMSprop
	model = Sequential()
	model.add(Conv1D(32, 7, activation='relu', input_shape=input_train.shape))
	model.add(MaxPooling1D(3))
	model.add(Conv1D(32, 7, activation='relu'))
	model.add(GRU(32, dropout=0.1, recurrent_dropout=0.5))
	model.add(Dense(1))
	model.summary()
	model.compile(optimizer=RMSprop(lr=1e-4), loss='binary_crossentropy', metrics=['acc'])
	history = model.fit(input_train, y_train, epochs=10, batch_size=128, validation_split=0.2)


