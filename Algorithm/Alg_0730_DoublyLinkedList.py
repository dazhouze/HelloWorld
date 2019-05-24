#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class _DoublyLinkedBase(object):
	'''A base class providing a doubly linked list representation.'''

	##### _Node class #####
	class _Node(object):
		'''Lightweigth, nonpublic class for storing a double linked node.'''
		__slots__ = '_element', '_prev', '_next'

		def __init__(self, e, p, n):
			self._element = e
			self._prev = p
			self._next = n

	##### doubly linked base class and method #####
	def __init__(self):
		'''Creat an empty list'''
		self._header = self._Node(None, None, None)
		self._trailer = self._Node(None, None, None)
		self._header._next = self._trailer
		self._trailer._prev = self._header
		self._size = 0

	def __len__(self):
		'''Return the number of elements in the list.'''
		return self._size

	def is_empty(self):
		'''Return True if the list is empty.'''
		return self._size == 0

	def _insert_between(self, e, predecessor, successor):
		'''Add element e between two existing nodes and return new node.'''
		newest = self._Node(e, predecessor, successor)
		predecessor._next = newest
		successor._prev = newest
		self._size += 1
		return newest

	def _delete_node(self, node):
		'''Delete nonsentinel node from the list and returen its element.'''
		predecessor = node._prev
		successor = node._next
		predecessor._next = successor
		successor._prev = predecessor
		self._size -= 1
		element = node._element
		node._prev = None
		node._next = None
		node._element = None
		return element

if __name__ == '__main__':
	pass
