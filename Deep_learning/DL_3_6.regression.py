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

def build_model():
	from keras import models
	from keras import layers
	model = models.Sequential()
	model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(1))
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
	return model

def smooth_curve(points, factor=0.9):
	smoothed_points = []
	for point in points:
		if smoothed_points:
			previous = smoothed_points[-1]
			smoothed_points.append(previous * factor + point*(1-factor))
		else:
			smoothed_points.append(point)
	return smoothed_points

if __name__ == '__main__':
	from keras.datasets import boston_housing
	(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()
	print(train_data.shape)
	print(test_data.shape)
	mean = train_data.mean(axis=0)
	std = train_data.std(axis=0)
	train_data = (train_data-mean)/std
	test_data = (test_data-mean)/std
	
	k = 4  # K-fold validataion
	num_val_samples = len(train_data) // k
	num_epochs = 500
	all_mae_history = []
	for i in range(k):
		print('processing fold #', i)
		val_data = train_data[i*num_val_samples: (i+1)*num_val_samples]
		val_targets = train_targets[i*num_val_samples: (i+1)*num_val_samples]
		partial_train_data = np.concatenate([train_data[:i*num_val_samples], train_data[(i+1)*num_val_samples:]], axis=0)
		partial_train_targets = np.concatenate([train_targets[:i*num_val_samples], train_targets[(i+1)*num_val_samples:]], axis=0)
		model = build_model()
		history = model.fit(partial_train_data, partial_train_targets, validation_data=(val_data, val_targets), epochs=num_epochs, batch_size=1, verbose=0)
		mae_history = history.history['val_mean_absolute_error']
		all_mae_history.append(mae_history)

	average_mae_history = [np.mean([x[i] for x in all_mae_history]) for i in range(num_epochs)]

	with matplotlib.backends.backend_pdf.PdfPages('DL_3_6.pdf') as pdf_all: 
		fig = plt.figure()
		plt.plot(range(1, len(average_mae_history)+1), average_mae_history, 'b')  # blue line
		#plt.title('Training and validation loss', fontsize=20)
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Validation MAE', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		#plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)

		fig = plt.figure()
		smooth_mae_history = smooth_curve(average_mae_history[10:])
		plt.plot(range(1, len(smooth_mae_history)+1), smooth_mae_history, 'b')
		#plt.title('Training and validation loss', fontsize=20)
		plt.xlabel('Epochs', fontsize=20)
		plt.ylabel('Validation MAE', fontsize=20)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		#plt.legend()
		plt.tight_layout()
		pdf_all.savefig(fig)

	model = build_model()
	model.fit(train_data, train_targets, epochs=80, batch_size=16, verbose=0)
	test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)
	model.save('./DL_3_6.h5')
	print(test_mae_score)
