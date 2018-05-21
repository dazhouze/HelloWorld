#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import os
import tensorflow as tf
import keras

if __name__ == '__main__':

	from keras.applications import VGG16
	conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
	conv_base.summary()
	'''
	# extract features from these images by calling the predict method of the conv_base model
	# extracting features useing the pretrainded convolutional base
	from keras.preprocessing.image import ImageDataGenerator
	base_dir = 'cats_and_dogs_small'
	train_dir = os.path.join(base_dir, 'train')
	validation_dir = os.path.join(base_dir, 'validation')
	test_dir = os.path.join(base_dir, 'test')
	datagen = ImageDataGenerator(rescale=1./255)
	batch_size = 20

	def extract_features(directory, sample_count):
		features = np.zeros(shape=(sample_count, 4, 4, 512))
		labels = np.zeros(shape=(sample_count))
		generator = datagen.flow_from_directory(directory, target_size=(150, 150), batch_size=batch_size, class_mode='binary')
		i = 0
		for inputs_batch, labels_batch in generator:
			features_batch = conv_base.predict(inputs_batch)
			features[i * batch_size : (i+1) * batch_size] = features_batch
			labels[i * batch_size : (i+1) * batch_size] = labels_batch
			i += 1
			if i * batch_size >= sample_count:
				break
		return features, labels

	train_features, train_labels = extract_features(train_dir, 2000)
	validation_features, validation_labels = extract_features(validation_dir, 1000)
	test_features, test_labels = extract_features(test_dir, 1000)
	train_features = np.reshape(train_features, (2000, 4 * 4 *512))
	validation_features = np.reshape(validation_features, (1000, 4 * 4 * 512))
	test_features = np.reshape(test_features, (1000, 4 * 4 * 512))

	from keras import models
	from keras import layers
	from keras import optimizers
	model = models.Sequential()
	model.add(layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(1, activation='sigmoid'))

	model.compile(optimizer=optimizers.RMSprop(lr=2e-5), loss='binary_crossentropy', metrics=['acc'])
	hisotory = model.fit(train_features, train_labels, epochs=30, batch_size=20, validation_data=(validation_features, validation_labels))
	'''

	# extending the conv_base model and running it end to end on the inputs.
	# GPU only
	from keras import models
	from keras import layers
	model = models.Sequential()
	model.add(conv_base)
	model.add(layers.Flatten())
	model.add(layers.Dense(256, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.summary()
	print('This is the number of trainable weights ' 'before freezing the conv base:', len(model.trainable_weights))
	conv_base.trainable = False
	print('This is the number of trainable weights ' 'ater freezing the conv base:', len(model.trainable_weights))

	from keras.preprocessing.image import ImageDataGenerator
	from keras import optimizers
	train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
	test_datagen = ImageDataGenerator(rescale=1./255)
	train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
	validation_generator = test_datagen.flow_from_directory(validation_dir, train_size(150, 150), batch_size=20, class_mode='binary')
	model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
	history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=30, validation_data=validation_generator, validation_step=50)
