#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import numpy as np
import pandas as pd
import torch

if __name__ == '__main__':
	# scalar 0-D tensor
	x = torch.rand(10)  # 10 items
	print(x, x.size())

	# vector 1-D tensor
	temp = torch.FloatTensor([23, 24.5, 25, 26])
	print(temp, temp.size())

	# matrix 2-D tensor
	boston_tensor = torch.rand(506, 13)
	print(boston_tensor.size())

	# 3-D tensor
	# image 224,224,3

	# slicing tensors
	sales = torch.eye(3, 3)
	print(sales, sales[0,1],)

	# 4-D tensor
	# batch of images. common batch size: 16, 32, 64

	# 5-D tensor
	# video data

	# tensor addation
	a = torch.rand(2, 2)
	b = torch.rand(2, 2)
	c = a + b
	d = torch.add(a, b)
	print(c, '\n', d)
	print(a)
	a.add_(5)  # inplace
	print(a)

	# tensor multiplication
	a = torch.rand(10**4, 10**4)
	b = torch.rand(10**4, 10**4)
	a.mul(b)
	a.mul_(b)  # in-place
