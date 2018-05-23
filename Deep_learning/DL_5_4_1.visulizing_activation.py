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
	with matplotlib.backends.backend_pdf.PdfPages('DL_5_4_1.pdf') as pdf_all: 
		from keras.models import load_model
		model = load_model('cats_and_dogs_small_2.h5')

		from keras.applications import VGG16
		conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
		conv_base.summary()
		model = conv_base

		model.summary()
		
		img_path = 'cats_and_dogs_small/test/cats/cat.1700.jpg'
		from keras.preprocessing import image
		img = image.load_img(img_path, target_size=(150, 150))
		img_tensor = image.img_to_array(img)
		img_tensor = np.expand_dims(img_tensor, axis=0)
		img_tensor /= 255.

		print(img_tensor.shape)
		fig = plt.figure()
		plt.imshow(img_tensor[0])
		pdf_all.savefig()

		from keras import models
		layer_outputs = [layer.output for layer in model.layers[:8]]
		activation_model = models.Model(inputs=model.input, outputs=layer_outputs)
		activations = activation_model.predict(img_tensor)

		first_layer_activation = activations[0]
		print(first_layer_activation.shape)

		fig = plt.figure()
		plt.matshow(first_layer_activation[0, :, :, 0], cmap='viridis')
		pdf_all.savefig()

		fig = plt.figure()
		plt.matshow(first_layer_activation[0, :, :, 1], cmap='viridis')
		pdf_all.savefig()

		layer_names = []
		for layer in model.layers[:8]:
			layer_names.append(layer.name)
		images_per_row = 16
		for layer_name, layer_activation in zip(layer_names, activations):
			fig = plt.figure()
			n_features = layer_activation.shape[-1]
			size = layer_activation.shape[1]
			n_cols = n_features // images_per_row
			display_grid= np.zeros((size*n_cols, images_per_row*size))
			for col in range(n_cols):
				for row in range(images_per_row):
					channel_image = layer_activation[0, :, :, col*images_per_row + row]
					channel_image -= channel_image.mean()
					channel_image /= channel_image.std()
					channel_image *= 64
					channel_image += 128
					channel_image = np.clip(channel_image, 0 , 255).astype('uint8')
					display_grid[col*size : (col+1)*size, row*size:(row+1)*size] = channel_image
			scale = 1./size
			plt.figure(figsize=(scale*display_grid.shape[1], scale*display_grid.shape[0]))
			plt.title(layer_name)
			plt.grid(False)
			plt.imshow(display_grid, aspect='auto', cmap='viridis')
			pdf_all.savefig()
