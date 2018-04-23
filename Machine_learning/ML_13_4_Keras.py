#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
#import tensorflow.keras as keras
import keras
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

if __name__ == '__main__':
	mnist = np.load('mnist_scaled.npz')
	X_train, X_test, y_train, y_test = mnist['X_train'], mnist['X_test'], mnist['y_train'], mnist['y_test']

	mean_vals = np.mean(X_train, axis=0)
	std_val = np.std(X_train)
	X_train_centered = (X_train - mean_vals)/std_val
	X_test_centered = (X_test - mean_vals)/std_val
	del X_train, X_test
	np.random.seed(123)
	tf.set_random_seed(123)

	y_train_onehot = keras.utils.to_categorical(y_train)  # one hot
	print('First 3 labels: ', y_train[:3])
	print('First 3 labels: ', y_train_onehot[:3])

	model = keras.models.Sequential()
	model.add(keras.layers.Dense(units=50, input_dim=X_train_centered.shape[1], kernel_initializer='glorot_uniform', bias_initializer='zeros', activation='tanh'))
	model.add(keras.layers.Dense(units=50, input_dim=50, kernel_initializer='glorot_uniform', bias_initializer='zeros', activation='tanh'))
	model.add(keras.layers.Dense(units=y_train_onehot.shape[1], input_dim=50, kernel_initializer='glorot_uniform', bias_initializer='zeros', activation='softmax'))
	sgd_optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-7, momentum=0.9)
	model.compile(optimizer=sgd_optimizer, loss='categorical_crossentropy')

	history = model.fit(X_train_centered, y_train_onehot, batch_size=64, epochs=50, verbose=1, validation_split=0.1)

	y_train_pred = model.predict_classes(X_train_centered, verbose=0)
	correct_preds = np.sum(y_train==y_train_pred, axis=0)
	train_acc = correct_preds / y_train.shape[0]
	print('Training accuracy: %.2f%%' % (train_acc*100))
	y_test_pred = model.predict_classes(X_test_centered, verbose=0)
	correct_preds = np.sum(y_test==y_test_pred, axis=0)
	test_acc = correct_preds/y_test.shape[0]
	print('Test accuracy: %.2f%%' % (test_acc*100))
