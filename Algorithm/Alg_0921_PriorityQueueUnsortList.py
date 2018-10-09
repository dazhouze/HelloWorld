#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0742_PositionalList import PositionalList
class UnsortedPriorityQueue(object):
	''' A min-oriented priority queue implemented with an un sorted list.'''
	class _Item(object):
		'''Lightweight composite to store priority queue items.'''
		__slots__ = '_key', '_value'

		def __init__(self, k, v):
			self._key = k
			self._value = v

		def __lt__(self, other):
			'''Redefine __lt__ to compare 2 _Item instance based on _key'''
			return self._key < other._key

		def get_key(self):
			'''Return key of _Item'''
			return self._key

		def get_value(self):
			'''Return value of _Item'''
			return self._value

	def _find_min(self):
		'''Return Position of item with minimum key.'''
		if self.is_empty():
			raise Empty('Priority queue is empty')
		small = self.__data.first()
		walk = self.__data.after(small)
		while walk is not None:
			if walk.get_element() < small.get_element():
				small = walk
			walk = self.__data.after(walk)
		return small

	def __init__(self):
		'''Creat a new empty Priority Queue.'''
		self.__data = PositionalList()

	def __len__(self):
		'''Return the number of items in the priority queue.'''
		return len(self.__data)

	def is_empty(self):
		'''Return True if the priority queue is empyt'''
		return len(self.__data) == 0

	def add(self, key, value):
		'''Add a key-value pair.'''
		self.__data.add_last(self._Item(key, value))

	def min(self):
		'''Return but do not remeve (k, v) tuple with minimum key.'''
		p = self._find_min()
		item = p.get_element()
		return (item.get_key(), item.get_value())

	def remove_min(self):
		'''Remove and return (k, v) tuple with minmum key.'''
		p = self._find_min()
		item = self.__data.delete(p)
		return (item.get_key(), item.get_value())

if __name__ == '__main__':
	USL = UnsortedPriorityQueue()
	USL.add(1, 11)
	USL.add(3, 13)
	USL.add(5, 15)
	USL.add(1, 12)
	print(USL.min())
	print(USL.remove_min())
	print(USL.min())
