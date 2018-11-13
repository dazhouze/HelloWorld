#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0934_PriorityQueueHeapArray import HeapPriorityQueue
class AdaptableHeapPriorityQueue(HeapPriorityQueue):
	'''A locator-based priority queue implemented with a binary heap.'''
	class Locator(HeapPriorityQueue._Item):
		'''Token for locating an entry of the priority queue.'''
		__slots__ = '_index'

		def __init__(self, k, v, j):
			super().__init__(k, v)
			self._index = j

	def _swap(self, i, j):
		'''Swap the element at indices i and j of array.'''
		super()._swap(i, j)
		self._data[i]._index, self._data[j]._index = i, j

	def _bubble(self,j):
		if j > 0 and self._data[j] < self._data[self._parent(j)]:
			sefl._upheap(j)
		else:
			self._downheap(j)

	def add(self, key, value):
		'''Add a key-value pair to the priority queue.'''
		token = self.Locator(key, value, len(self._data))
		self._data.append(token)
		self._upheap(len(self._data) - 1)
		return token

	def update(self, loc, new_key, new_val):
		'''Update the key and value for the entry indextified by Locator loc.'''
		j = loc._index
		if not (0 <= j < len(self) and self._data[j] is loc):
			raise ValueError('Invalid locator')
		loc._key, loc._value = new_key, new_val
		self._bubble(j)

	def remove(self, loc):
		'''Remove and return the (k, v) pair identified by Locator loc.'''
		j = loc._index
		if not (0 <= j < len(self) and self._data[j] is loc):
			raise ValueError('Invalid locator')
		if j == len(self) - 1:
			self._data.pop()
		else:
			self._swap(j, len(self) - 1)
			self._data.pop()
			self._bubble(j)
		return (loc._key, loc._value)

if __name__ == '__main__':
	AHPQ = AdaptableHeapPriorityQueue()
	loc1 = AHPQ.add(1, 11)
	loc2 = AHPQ.add(3, 13)
	loc3 = AHPQ.add(5, 15)
	loc4 = AHPQ.add(1, 12)
	print(len(AHPQ))
	print(AHPQ.min())
	print(AHPQ.remove_min())
	print(len(AHPQ))
	AHPQ.remove(loc3)
	print(len(AHPQ))
