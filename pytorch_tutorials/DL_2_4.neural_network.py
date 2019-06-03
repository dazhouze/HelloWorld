#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import pandas as pd
import torch
from torch.autograd import Variable

def get_data():
	'''Creat data for neural network.
	train data and labels.
	'''
	train_X = np.array([
		3.3, 4.4, 5.5, 6.7, 6.9, 4.1, 9.7, 6.1, 7.5, 2.1, 7.0, 10.7, 5.3, 7.9, 5.6, 9.2, 3.1
		])
	train_Y = np.array([
		1.7, 2.7, 2.0, 3.1, 1.6, 1.5, 3.3, 2.5, 2.5, 1.2, 2.8, 3.4, 1.6, 2.9, 2.4, 2.9, 1.3
		])
	dtype = torch.FloatTensor
	X = Variable(torch.from_numpy(train_X).type(dtype), requires_grad=False).view(17, 1)
	y = Variable(torch.from_numpy(train_Y).type(dtype), requires_grad=False)
	return X, y

def get_weights():
	'''Creat learnable parameters.
	'''
	w = Variable(torch.randn(1), requires_grad=True)
	b = Variable(torch.randn(1), requires_grad=True)
	return w, b

def simple_network(x):
	y_pred = torch.matmul(x, w) + b  # Matrix product of two tensors
	return y_pred

def loss_fn(y, y_pred):
	loss = (y_pred - y).pow(2).sum()
	for param in (w, b):
		if not param.grad is None:
			param.grad.data.zero_()
	loss.backward()
	return loss.data[0]

if __name__ == '__main__':
	# y = wx + b
	x, y = get_data()  # x -> training data, y -> target variables
	w, b = get_weights()  # weight and bias
	
	for i in range(500):
		y_pred = simple_network(x)  # func which computes: wx + b
		loss = loss_fn(y, y_pred)  # calculates sum of squared diff of y and y_pred
		if i % 50 == 0:
			print(loss)
		optimize(learing_rate)  # adjust w, b to minimize the loss
