#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ArrayQueue(object):
	'''FIFO queue implementation using a Python list as underlying storages.'''
	DEFAULT_CAPACITY = 10 # moderate for all new queues

	def __init__(self):
		'''Create an empty queue'''
		self._data = [None] * ArrayQueue.DEFAULT_CAPACITY # constant in class need to be annoanced
		self._size = 0
		self._front = 0

	def __len__(self):
		'''Retrun the number of elemetns in the queue'''
		return self._size

	def is_empty(self):
		'''Return True if the queue is empty'''
		return self._size == 0

	def first(self):
		'''
		Return (but do not remove) the element at the front of the queue
		Raise Empty excepython if the queue is empty
		'''
		if self.is_empty():
			raise IndexError('Queue is empty.')
		return self._data[self._front]

	def dequeue(self):
		'''
		Remove and return the first element of the queue
		Raise Empty excepyion if the queue is empty
		'''
		if self.is_empty():
			raise IndexError('Queue is empty.')
		answer = self._data[self._front]
		self._data[self._front] = None
		self._front = (self._front+1)%len(self._data)
		self._size -= 1
		'''shrringking the underlying array'''
		if 0 < self._size< len(self._data)//4:
				self._resize(len(self._data)//2)
		return answer

	def enqueue(self, e):
		'''Add an element to the back of queue'''
		if self._size == len(self._data):
			self._resize(2*self._size)
		avail = (self._front + self._size) % len(self._data)
		self._data[avail] = e
		self._size += 1

	def _resize(self, cap):
		'''Resize to a new list of capaciyt'''
		old = self._data
		self._data = [None] * cap
		walk = self._front
		for k in range(0, self._size):
			self._data[k] = old[walk]
			walk = (1+walk) % len(old)
		self._front = 0


if __name__ == '__main__':
	AQ = ArrayQueue()
	for i in range(19):
		AQ.enqueue(i)
		print("enqueue:%d, size:%d"%(i,len(AQ)))
	for i in range(18,0,-1):
		print('first: %d dequeue: %d, next: %d'%(AQ.first(), AQ.dequeue(), AQ.first()))
