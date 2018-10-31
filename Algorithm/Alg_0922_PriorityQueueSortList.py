#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0742_PositionalList import PositionalList
from Alg_0921_PriorityQueueUnsortList import PriorityQueueBase

class SortedPriorityQueue(PriorityQueueBase):
	''' A min-oriented priority queue implemented with an un sorted list.'''
	def __init__(self):
		'''Creat a new empty Priority Queue.'''
		self._data = PositionalList()

	def __len__(self):
		'''Return the number of items in the priority queue.'''
		return len(self._data)

	def add(self, key, value):
		'''Add a key-value pair.'''
		newest = self._Item(key, value)
		walk = self._data.last()  # walk backward looking for smaller key 
		while walk is not None and newest < walk.get_element():
			walk = self._data.before(walk)
		if walk is None:
			self._data.add_first(newest)
		else:
			self._data.add_after(walk, newest)

	def min(self):
		'''Return but do not remeve (k, v) tuple with minimum key.'''
		if self.is_empty():
			raise Empty('Priority queue is empty.')
		p = self._data.first()
		item = p.get_element()
		return (item._key, item._value)

	def remove_min(self):
		'''Remove and return (k, v) tuple with minmum key.'''
		if self.is_empty():
			raise Empty('Priority queue is empty.')
		item = self._data.delete(self._data.first())
		return (item._key, item._value)

if __name__ == '__main__':
	SL = SortedPriorityQueue()
	SL.add(1, 12)
	SL.add(1, 11)
	SL.add(3, 13)
	SL.add(5, 15)
	print(SL.min())
	print(SL.remove_min())
	print(SL.min())
