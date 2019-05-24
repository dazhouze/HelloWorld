#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
https://www.tensorflow.org/tutorials/keras/basic_regression
'''

# modules for pdf plot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import seaborn as sns
# modules for TensorFlow
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

class PrintDot(keras.callbacks.Callback):
	'''Display training progress, one dot a epoch, 100 dots a line'''
	def on_epoch_end(self, epoch, logs):
		if epoch % 100 == 0:
			print('')
		print('.', end='')

def regression():
	# homes in a Boston suburb during the mid-1970s
	boston_housing = keras.datasets.boston_housing
	(train_data, train_labels), (test_data, test_labels) = boston_housing.load_data()

	# explore the data
	print('\nTraining entries: {}, labels: {}'.format(len(train_data), len(train_labels)))
	print('Training data No.1:\n', train_data[0])
	#The dataset contains 13 different features:
	#Per capita crime rate.
	#The proportion of residential land zoned for lots over 25,000 square feet.
	#The proportion of non-retail business acres per town.
	#Charles River dummy variable (= 1 if tract bounds river; 0 otherwise).
	#Nitric oxides concentration (parts per 10 million).
	#The average number of rooms per dwelling.
	#The proportion of owner-occupied units built before 1940.
	#Weighted distances to five Boston employment centers.
	#Index of accessibility to radial highways.
	#Full-value property-tax rate per $10,000.
	#Pupil-teacher ratio by town.
	#1000 * (Bk - 0.63) ** 2 where Bk is the proportion of Black people by town.
	#Percentage lower status of the population.

	# Suffle the training set
	order = np.argsort(np.random.random(train_labels.shape))  # random index array
	train_data = train_data[order]
	train_labels = train_labels[order]
	
	# column name of data features
	column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
	df = pd.DataFrame(train_data, columns=column_names)
	print('\nHead of data frame:\n', df.head())

	# Normalize features
	mean, std = train_data.mean(axis=0), train_data.std(axis=0)
	train_data = (train_data - mean) / std  # scaled independently
	test_data = (test_data - mean) / std  # scaled independently
	print('Normalized training data No.1:\n', train_data[0])

	# first model
	def build_model():
		model = keras.Sequential()
		model.add(keras.layers.Dense(
			64, activation=tf.nn.relu,
			input_shape = (train_data.shape[1],)
			))
		model.add(keras.layers.Dense(
			64, activation=tf.nn.relu
			))
		model.add(keras.layers.Dense(1))
		
		# compile model
		model.compile(loss='mse',
				optimizer=tf.train.RMSPropOptimizer(0.001),
				metrics=['mae'])
		return model
	model = build_model()
	model.summary()
	
	EPOCHS = 500
	history = model.fit(
			train_data, train_labels,
			epochs=500,
			validation_split=0.2,
			verbose=0,
			callbacks=[PrintDot()]
			)
	
	# plot loss
	def plot_history(history, pdf_file='TF.pdf'):
		with matplotlib.backends.backend_pdf.PdfPages('TF.pdf') as pdf_all:
			epochs = range(1, len(np.array(history.history['mean_absolute_error']))+1)
			fig = plt.figure()
			plt.plot(epochs, np.array(history.history['mean_absolute_error']), color='blue', marker=',', label='Training loss')
			plt.plot(epochs, np.array(history.history['val_mean_absolute_error']), color='orange', marker=',', label='Validation loss')
			plt.xticks(fontsize=15)
			plt.yticks(fontsize=15)							
			plt.ylabel('Mean Abs Error [1000$]', fontsize=20)
			plt.xlabel('Epochs', fontsize=20)
			plt.legend(frameon=False, fontsize=15)
			plt.ylim(0, 5)
			plt.tight_layout()
			pdf_all.savefig(fig)						   		

	plot_history(history)

	# Evaluation 
	loss, mae = model.evaluate(test_data, test_labels, verbose=0)
	print("Testing set Mean Abs Error: ${:7.2f}".format(mae * 1000))

	# Predict
	test_predictions = model.predict(test_data).flatten()  # flatten: [[x],[y],[z]] -> [x,y,z]
	error = test_predictions - test_labels  # predict error
	with matplotlib.backends.backend_pdf.PdfPages('TF2.pdf') as pdf_all:
		# True - prediction
		fig = plt.figure()
		plt.scatter(test_labels, test_predictions, color='blue', marker='o', alpha=0.8)
		plt.plot([0, 60], [0, 60], linestyle='--')  # diagonal line
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)							
		plt.ylabel('Predicted mean Abs Error [1000$]', fontsize=20)
		plt.xlabel('True mean Abs Error [1000$]', fontsize=20)
		plt.tight_layout()
		pdf_all.savefig(fig)						   		
		# error hist
		fig = plt.figure()
		plt.hist(error, bins=50, color='blue', alpha=0.8)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)							
		plt.xlabel('Prediction error [1000$]', fontsize=20)
		plt.ylabel('Count', fontsize=20)
		plt.tight_layout()
		pdf_all.savefig(fig)						   		




if __name__ == '__main__':
	print('TensorFlow version', tf.__version__)
	print('Keras version', keras.__version__)
	regression()
