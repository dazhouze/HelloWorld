#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import tensorflow as tf
import keras
from keras import backend as K

if __name__ == '__main__':
	from keras.applications.vgg16 import VGG16
	model = VGG16(weights='imagenet')  # include densely connected classifier
	from keras.preprocessing import image
	from keras.applications.vgg16 import preprocess_input, decode_predictions
	img_path = 'creative_commons_elephant.jpg'
	img = image.load_img(img_path, target_size=(224, 224))
	x = image.img_to_array(img)
	print(x.shape)
	x = np.expand_dims(x, axis=0)
	print(x.shape)
	x = preprocess_input(x)
	
	preds = model.predict(x)
	print('Predicted:', decode_predictions(preds, top=3)[0])

	# setup Grad-CAM algorithm
	african_elephant_output = model.output[:, 386]
	last_conv_layer = model.get_layer('block5_conv3')
	grads = K.gradients(african_elephant_output, last_conv_layer.output)[0]
	pooled_grads = K.mean(grads, axis=(0, 1, 2))
	iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
	pooled_grads_value, conv_layer_output_value = iterate([x])
	for i in range(512):
		conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
	heatmap = np.mean(conv_layer_output_value, axis=-1)
	heatmap = np.maximum(heatmap, 0)
	heatmap /= np.max(heatmap)
	with matplotlib.backends.backend_pdf.PdfPages('DL_5_4_3.pdf') as pdf_all: 
		fig = plt.figure()
		plt.matshow(heatmap)
		pdf_all.savefig()

	import cv2
	img = cv2.imread(img_path)
	heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
	heatmap = np.uint8(255*heatmap)
	heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
	superimposed_img = heatmap * 0.4 + img
	cv2.imwrite('elephant_cam2.jpg', superimposed_img)
