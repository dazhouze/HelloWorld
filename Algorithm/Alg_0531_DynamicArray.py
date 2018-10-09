#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes

class DynamicArray(object):
	'''A dynamic array class akin to a simplified Python list'''
	def __init__(self):
	    '''Create an empty array'''
	    self._n = 0 # to count actual elements
	    self._capacity = 1 # default array capacity
	    self._A = self._make_array(self._capacity) #low-level array

	def __len__(self):
	    '''Return num of elements store in the array.'''
	    return self._n

	def __getitem__(self, k):
	    '''Return element at index k'''
	    if not 0 <=k < self._n:
	        raise IndexError('Invalid index!')
	    return self._A[k]

	def get_capacity(self):
	    '''return the capacity of array'''
	    return self._capacity

	def append(self, obj):
	    '''Add object to end of the array.'''
	    if self._n == self._capacity:
	        self._resize(2 * self._capacity)
	    self._A[self._n] = obj
	    self._n += 1

	def _resize(self, c):
	    '''Resize internal array to capacity c'''
	    B = self._make_array(c)
	    for k in range(0, self._n):
	        B[k] = self._A[k]
	    self._A = B
	    self._capacity = c

	def _make_array(self, c):
	    '''Return new arrya with capacity c'''
	    return (c *  ctypes.py_object)()

if __name__ == '__main__':
	a = DynamicArray() 
	for x in range(1, 30):
	    a.append(x)
	    print('array length:%d\tcapacity:%d' % (len(a), a.get_capacity()))
