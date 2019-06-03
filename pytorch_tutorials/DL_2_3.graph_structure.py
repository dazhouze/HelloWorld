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

if __name__ == '__main__':

	x = Variable(torch.ones(2, 2), requires_grad=True)
	y = x.mean()
	
	y.backward()
	
	print(x.grad)
	print(x.data)
	print(y.grad_fn)
	
