#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
https://www.tensorflow.org/tutorials/keras/basic_text_classification
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

def text_classify():
	# IMDB dataset, 50,000 movie reviews from the Internet Movie Database. 25,000 reviews for training and 25,000 for testing
	imdb = keras.datasets.imdb
	(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
	# explore the data
	print('\nTraining entries: {}, labels: {}'.format(len(train_data), len(train_labels)))
	print('Training data No.1:\n', train_data[0])

	# Convert the integers back to words
	word_index = imdb.get_word_index()
	word_index["<PAD>"], word_index["<START>"], word_index["<UNK>"], word_index["<UNUSED>"] = 0, 1, 2, 3  # some key word
	word_index = {k:(v+3) for k,v in word_index.items()}  # other words
	reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
	def decode_review(text):
		'''decode integer to text.'''
		return ' '.join([reverse_word_index.get(i, '?') for i in text])
	print('Training data No.1:\n', decode_review(train_data[0]))
	
	# Prepare the data
	train_data = keras.preprocessing.sequence.pad_sequences(train_data, 
			value=word_index["<PAD>"],
			padding='post',
			maxlen=256)  # pad the arrays so they all have the same length
	test_data = keras.preprocessing.sequence.pad_sequences(test_data, 
			value=word_index["<PAD>"],
			padding='post',
			maxlen=256)  # pad the arrays so they all have the same length
	print('\nLength of train and test', len(train_data[0]), len(train_data[1]))

	# Build the model
	vocab_size = 10000  # vocabulary count used for the movie reviews (10,000 words)
	model = keras.Sequential()
	model.add(keras.layers.Embedding(vocab_size, 16))
	model.add(keras.layers.GlobalAveragePooling1D())  # fixed-length output
	model.add(keras.layers.Dense(16, activation=tf.nn.relu))  # fully connected node
	model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))  # densely connected
	model.summary()

	# Loss func and optimizer
	model.compile(loss='binary_crossentropy',  # binary_crossentropy is better for dealing with probabilities
			optimizer=tf.train.AdamOptimizer(),
			metrics=['accuracy'])

	# Create a validation set
	x_val, partial_x_train = train_data[:10000], train_data[10000:]
	y_val, partial_y_train = train_labels[:10000], train_labels[10000:]
	print('\nNumber of validation set', len(x_val))
	print('Number of train set', len(partial_x_train))

	# Train the model
	history = model.fit(
			partial_x_train,
			partial_y_train,
			epochs=40,
			batch_size=512,
			validation_data=(x_val, y_val),
			verbose=1
			)

	# Results
	results = model.evaluate(test_data, test_labels)  # loss, acc
	print(results)

	# Evaluate the model
	history_dict = history.history
	print('history keys', history_dict.keys())

	loss, acc, val_loss, val_acc = history.history['loss'],  history.history['acc'], history.history['val_loss'], history.history['val_acc']  # loss and accuracy in train and validation set
	epochs = range(1, len(acc)+1)
	with matplotlib.backends.backend_pdf.PdfPages('TF.pdf') as pdf_all:
		fig = plt.figure()
		plt.plot(epochs, acc, color='blue', marker='o', label='Training accuracy')
		plt.plot(epochs, val_acc, color='green', marker='o', label='Validation accuracy')
		plt.plot(epochs, loss, color='blue', marker='^', label='Training loss')
		plt.plot(epochs, val_loss, color='green', marker='^', label='Validation loss')
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)							
		plt.ylabel('Accuracy', fontsize=20)
		plt.xlabel('Epochs', fontsize=20)
		plt.legend(frameon=False, fontsize=15)
		plt.tight_layout()
		pdf_all.savefig(fig)						   		

if __name__ == '__main__':
	print('TensorFlow version', tf.__version__)
	print('Keras version', keras.__version__)
	text_classify()
