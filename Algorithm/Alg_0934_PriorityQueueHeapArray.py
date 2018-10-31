#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A heap is a binary tree T.
Heap order Property: A heap T, for every position p (other than root), the key strored at p is >= key at p's parant.
Complete binary tree property: A heap T with height h, levels 0 to h-1, maximum number of nodes, and remaining nodes at level h in leftmost possibel positions.
Insertion: upward movement, up-heap bubbling
Deletion: downward swapping, down-heap bubbling
'''

from Alg_0921_PriorityQueueUnsortList import PriorityQueueBase

class HeapPriorityQueue(PriorityQueueBase):
	''' A min-oriented priority queue implemented with a binary heap.'''
	def __init__(self):
		'''Creat a new empty Priority Queue.'''
		self._data = []

	def __len__(self):
		'''Return the number of items in the priority queue.'''
		return len(self._data)

	def _parent(self, j):
		return (j-1)//2

	def _left(self, j):
		return 2*j + 1

	def _right(self, j):
		return 2*j + 2
	
	def _has_left(self, j):
		return self._left(j) < len(self._data)

	def _has_right(self, j):
		return self._right(j) < len(self._data)

	def _swap(self, i, j):
		'''Swap the element at indices i and j of array.'''
		self._data[i], self._data[j] = self._data[j], self._data[i]

	def _upheap(self, j):
		'''When add _Item.'''
		parent = self._parent(j)
		if j > 0 and self._data[j] < self._data[parent]:
			self._swap(j, parent)
			self._upheap(parent)

	def _downheap(self, j):
		'''When rm min _Item.'''
		if self._has_left(j):
			left = self._left(j)
			small_child = left
			if self._has_right(j):
				right = self._right(j)
				if self._data[right] < self._data[left]:
					small_child = right
			if self._data[small_child] < self._data[j]:
				self._swap(j, small_child)
				self._downheap(small_child)

	def add(self, key, value):
		'''Add a key-value pair to the priority queue.'''
		self._data.append(self._Item(key, value))
		self._upheap(len(self._data) - 1)

	def min(self):
		'''Return but do not remove (k, v) tuple with minimum key.
		Raise Empth exception if empty.
		'''
		if self.is_empty():
			raise ValueError('Priority queue is empty.')
		item = self._data[0]
		return (item._key, item._value)

	def remove_min(self):
		'''Remove and return (k, v) tuple with minimum key.
		Raise ValueError exceptio if empty.
		'''
		if self.is_empty():
			raise ValueError('Priority queue is empty.')
		self._swap(0, len(self._data) - 1)
		item = self._data.pop()
		self._downheap(0)
		return (item._key, item._value)

if __name__ == '__main__':
	HPQ = HeapPriorityQueue()
	HPQ.add(1, 11)
	HPQ.add(3, 13)
	HPQ.add(5, 15)
	HPQ.add(1, 12)
	print(len(HPQ))
	print(HPQ.min())
	print(HPQ.remove_min())
	print(HPQ.min())
