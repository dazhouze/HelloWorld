#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
https://www.tensorflow.org/tutorials/keras/basic_classification
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

def basic_classify():
	# Fashion MNIST dataset which contains 70,000 grayscale images in 10 categories
	fashion_mnist = keras.datasets.fashion_mnist
	(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
	class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
			'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']  # index 0-9

	# explore the data
	print('\ntrain image shape', train_images.shape)
	print('train labels', train_labels)

	# Preprocess the data
	print('\ntype of a train image:', type(train_images[0]))
	print('shape of a train image:', train_images[0].shape)

	# scale these values to a range of 0 to 1
	train_images = train_images / 255.0
	test_images = test_images / 255.0

	with matplotlib.backends.backend_pdf.PdfPages('TF1.pdf') as pdf_all:
		fig = plt.figure()
		plt.imshow(train_images[0])  # np array to image
		plt.colorbar()
		plt.grid(False)
		pdf_all.savefig()
		# all catalog
		plt.figure(figsize=(10, 10))
		for i in range(25):
			plt.subplot(5, 5, i+1)  # 5*5, No.i
			plt.xticks([])  # hide xticks
			plt.yticks([])  # hide yticks
			plt.grid(False)  # hide grid
			plt.imshow(train_images[i], cmap=plt.cm.binary)  # np array to image
			plt.xlabel(class_names[train_labels[i]])  # train labels corresponding class name
		pdf_all.savefig()
	
	# Build the model
	model = keras.Sequential([
		keras.layers.Flatten(input_shape=train_images[0].shape),  # input layer, keras.layers.Flatten: 2D array to 1D
		keras.layers.Dense(128, activation=tf.nn.relu),  # densely/fully-connected neural layers with 128 nodes/neurons
		keras.layers.Dense(10, activation=tf.nn.softmax),  # output layer, nn number = catalog num
		])

	# Compile the model: 1. Loss function (how accurate), 2. Optimizer (how to update) and 3. Metrics (monitor train and test)
	model.compile(
			loss='sparse_categorical_crossentropy',
			optimizer=tf.train.AdamOptimizer(),
			metrics=['accuracy']
			)

	# Train the model: 1. Feed the train data, 2. Model learns and 3. Make prediction on test set
	model.fit(train_images, train_labels, epochs=5)  # feed the train data to model

	# Evaluate accuracy 
	test_loss, test_acc = model.evaluate(test_images, test_labels)
	print('\nTest loss', test_loss, 'Test accuracy', test_acc)

	# Make predictions
	predictions = model.predict(test_images)  # predictions / confidence array of all catalog
	print('\nFirst test data')
	print('predicted confidence', predictions[0])  # confidence array
	print('predicted result', np.argmax(predictions[0]), 'True restult', test_labels[0])  # index
	print('predicted result:', class_names[np.argmax(predictions[0])], 'True restult:', class_names[test_labels[0]])  # name

	# Plot image and confidence value
	with matplotlib.backends.backend_pdf.PdfPages('TF2.pdf') as pdf_all:
		num_rows, num_cols = 5, 3  # subplot number
		num_images = num_rows*num_cols
		plt.figure(figsize=(2*2*num_cols, 2*num_rows))
		for i in range(num_images):
			plt.subplot(num_rows, 2*num_cols, 2*i+1)
			plot_image(i, predictions, test_labels, test_images, class_names)
			plt.subplot(num_rows, 2*num_cols, 2*i+2)
			plot_value_array(i, predictions, test_labels, class_names)
		pdf_all.savefig()

def plot_image(i, predictions_array, true_label, img, class_names):
	'''Plot image and xticks.'''
	# for index i
	predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])
	plt.imshow(img, cmap=plt.cm.binary)  # plot
	predicted_label = np.argmax(predictions_array)  # predicted array to label
	color = 'blue' if predicted_label == true_label else 'red'  # true: blue, false: red
	plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label], 
		100*np.max(predictions_array),  #  predictions confidence array to percentage
		class_names[true_label]),  # true label name
		color=color) #

def plot_value_array(i, predictions_array, true_label, class_names):
	'''Plot predicted confidence array barplot.'''
	predictions_array, true_label = predictions_array[i], true_label[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])
	predicted_label = np.argmax(predictions_array)  # predicted reult color in red, else blue
	#sns.barplot(class_names, predictions_array, palette=['blue' if x == predicted_label else 'red' for x in range(len(predictions_array)) ])
	sns.barplot([x for x in range(len(predictions_array))], predictions_array, palette=['blue' if x == predicted_label else 'grey' for x in range(len(predictions_array)) ])
	plt.ylim([0, 1]) 

if __name__ == '__main__':
	print('TensorFlow version', tf.__version__)
	print('Keras version', keras.__version__)
	basic_classify()
