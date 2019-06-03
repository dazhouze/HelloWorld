#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# y = wx + b
x, y = get_data()  # x -> training data, y -> target variables
w, b = get_weights()  # weight and bias

for i in range(500):
	y_pred = simple_network(x)  # func which computes: wx + b
	loss = loss_fn(y, y_pred)  # calculates sum of squared diff of y and y_pred
	if i % 50 == 0:
		print(loss)
	optimize(learing_rate)  # adjust w, b to minimize the loss
