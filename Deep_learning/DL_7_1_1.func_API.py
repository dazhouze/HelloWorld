#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import keras

if __name__ == '__main__':
	from keras import Input, layers
	from keras.models import Sequential, Model
	model = Sequential()
	model.add(layers.Dense(32, activation='relu', input_shape=(64,)))
	model.add(layers.Dense(32, activation='relu'))
	model.add(layers.Dense(10, activation='softmax'))
	model.summary()

	input_tensor = Input(shape=(64,))
	x = layers.Dense(32, activation='relu')(input_tensor)
	x = layers.Dense(32, activation='relu')(x)
	output_tensor = layers.Dense(10, activation='softmax')(x)
	model = Model(input_tensor, output_tensor)
	model.summary()

	model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
	x_train = np.random.random((1000, 64))
	y_train = np.random.random((1000, 10))
	model.fit(x_train, y_train, epochs=10, batch_size=128)
	score = model.evaluate(x_train, y_train)
	print(score)

