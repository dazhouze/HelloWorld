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

	from keras import models
	from keras import layers
	model = models.Sequential()
	model.add(conv_base)
	model.add(layers.Flatten())
	model.add(layers.Dense(256, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))
	model.summary()

	conv_base.trainabel = True
	set_trainable = False
	for layer in conv_base.layers:
		if layer.name == 'block5_conv1':
			set_trainable = True
		if set_trainable:
			layer.trainable = True
		else:
			layer.trainable = False
	conv_base.summary()

	from keras.preprocessing.image import ImageDataGenerator
	from keras import optimizers
	base_dir = 'cats_and_dogs_small'
	train_dir = os.path.join(base_dir, 'train')
	validation_dir = os.path.join(base_dir, 'validation')
	test_dir = os.path.join(base_dir, 'test')
	train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
	test_datagen = ImageDataGenerator(rescale=1./255)
	train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
	validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=20, class_mode='binary')

	model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-5), metrics=['acc'])
	history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=100, validation_data=validation_generator, validation_steps=50)
	model.save('DL_5_4.fine_tuning.h5')

	test_generator = test_datagen.flow_from_dirctory(test_dir, target_size=(150, 150), bathc_size=20, class_mode='binary')
	test_loss, test_acc = model.evaluate_generator(test_generator, steps=50)
	print('test acc:', test_acc)
