#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import os
#import tensorflow as tf
import keras
from keras import backend as K

def deprocess_image(x):
	'''postprocess this tensor to turn it into a displayable image'''
	x -= x.mean()
	x /= (x.std() + 1e-5)
	x *= 0.1  # ensures std is 0.1
	x += 0.5
	x = np.clip(x, 0, 1)
	#x *= 255.
	#x = np.clip(x, 0, 255).astype('uint8')
	return x

def generate_pattern(modle, layer_name, filter_index, size=150):
	'''builds a loss func that maximizes the activation of the nth filter of the layer under consideration.'''
	layer_output = model.get_layer(layer_name).output
	loss = K.mean(layer_output[:, :, :, filter_index])
	grads = K.gradients(loss, model.input)[0]
	grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
	iterate = K.function([model.input], [loss, grads])
	input_img_data = np.random.random((1, size, size, 3)) * 20 + 128.
	step = 1
	for i in range(40):
		loss_value, grads_value = iterate([input_img_data])
		input_img_data += grads_value * step
	img = input_img_data[0]
	return deprocess_image(img)

if __name__ == '__main__':
	with matplotlib.backends.backend_pdf.PdfPages('DL_5_4_2.pdf') as pdf_all: 
		from keras.applications import VGG16
		model = VGG16(weights='imagenet', include_top=False)

		# filter vasulizations
		fig = plt.figure()
		plt.imshow(generate_pattern(model, 'block3_conv1', 0))
		pdf_all.savefig()

		# generate a grid of all filter reponse patterns in a layer
		layer_name = 'block1_conv1'
		size = 64
		margin = 5
		results = np.zeros((8*size + 7*margin, 8*size+7*margin, 3))
		for i in range(8):
			for j in range(8):
				filter_img = generate_pattern(model, layer_name, i+(j*8), size=size)
				horizontal_start = i*size + i*margin
				horizontal_end = horizontal_start + size
				vertical_start = j*size + j*margin
				vertical_end = vertical_start + size
				results[horizontal_start : horizontal_end, vertical_start: vertical_end, :] = filter_img
		fig = plt.figure()
		plt.figure(figsize=(20, 20))
		plt.imshow(results)
		pdf_all.savefig()
