#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes

class DynamicArray(object):
	'''A dynamic array class akin to a simplified Python list'''
	def __init__(self):
	    '''Create an empty array'''
	    self.__n = 0 # to count actual elements
	    self.__capacity = 1 # default array capacity
	    self.__A = self.__make_array(self.__capacity) #low-level array

	def __len__(self):
	    '''Return num of elements store in the array.'''
	    return self.__n

	def __getitem__(self, k):
	    '''Return element at index k'''
	    if not 0 <=k < self.__n:
	        raise IndexError('Invalid index!')
	    return self.__A[k]

	def getCapacity(self):
	    '''return the capacity of array'''
	    return self.__capacity

	def append(self, obj):
	    '''Add object to end of the array.'''
	    if self.__n == self.__capacity:
	        self.__resize(2 * self.__capacity)
	    self.__A[self.__n] = obj
	    self.__n += 1

	def __resize(self, c):
	    '''Resize internal array to capacity c'''
	    B = self.__make_array(c)
	    for k in range(0, self.__n):
	        B[k] = self.__A[k]
	    self.__A = B
	    self.__capacity = c

	def __make_array(self, c):
	    '''Return new arrya with capacity c'''
	    return (c *  ctypes.py_object)()

if __name__ == '__main__':
	a = DynamicArray() 
	for x in range(1, 30):
	    a.append(x)
	    print('array length:%d\tcapacity:%d' % (len(a), a.getCapacity()))
