#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedDequeue(object):
	'''A base class providing a doubly linked list representation.'''

	##### _Node class #####
	class _Node(object):
	    '''Lightweigth, nonpublic class for storing a double linked node.'''
	    __slots__ = '__element', '__prev', '__next'

	    def __init__(self, e, p, n):
	        self.__element = e
	        self.__prev = p
	        self.__next = n

	    def get_prev(self):
	        return self.__prev

	    def get_next(self):
	        return self.__next

	    def get_element(self):
	        return self.__element

	    def set_prev(self, p):
	        self.__prev = p

	    def set_next(self, n):
	        self.__next = n

	    def set_element(self, e):
	        self.__element = e

	##### doubly linked base class and method #####
	def __init__(self):
	    '''Creat an empty list'''
	    self.__header = self._Node(None, None, None)
	    self.__trailer = self._Node(None, None, None)
	    self.__header.set_next(self.__trailer)
	    self.__trailer.set_prev(self.__header)
	    self.__size = 0

	def __len__(self):
	    '''Return the number of elements in the list.'''
	    return self.__size

	def is_empty(self):
	    '''Return True if the list is empty.'''
	    return self.__size == 0

	def __insert_between(self, e, predecessor, successor):
	    '''Add element e between two existing nodes and return new node.'''
	    newest = self._Node(e, predecessor, successor)
	    predecessor.set_next(newest)
	    successor.set_prev(newest)
	    self.__size += 1
	    return newest

	def __delete_node(self, node):
	    '''Delete nonsentinel node from the list and returen its element.'''
	    predecessor = node.get_prev()
	    successor = node.get_next()
	    predecessor.set_next(successor)
	    successor.set_prev(predecessor)
	    self.__size -= 1
	    element = node.get_element()
	    node.set_prev(None)
	    node.set_next(None)
	    node.set_element(None)
	    return element

	def first(self):
	    '''Return (but do not remove) the element at the front of the deque.'''
	    if self.is_empty():
	        raise IndexError('Deque is empty')
	    return self.__header.get_next().get_element()

	def last(self):
	    '''Return (but do not remove) the element at the back of the deque.'''
	    if self.is_empty():
	        raise IndexError('Deque is empty.')
	    return self.__trailer.get_prev().get_element()

	def insert_first(self, e):
	    '''Add an element to the front of the deque.'''
	    self.__insert_between(e, self.__header, self.__header.get_next())

	def insert_last(self, e):
	    '''Add an element to the back of the deque.'''
	    self.__insert_between(e, self.__trailer.get_prev(), self.__trailer)

	def delete_first(self):
	    '''
	    Remove and return the element from the front of the deque.
	    Raise Empty exception if the deque is empty.
	    '''
	    if self.is_empty():
	        raise IndexError('Deque is empty.')
	    return self.__delete_node(self.__header.get_next())

	def delete_last(self):
	    '''
	    Remove and return the element from the back of the deque.
	    Raise Empty exception if the deque is empty.
	    '''
	    if self.is_empty():
	        raise IndexError('Deque is empty.')
	    return self.__delete_node(self.__trailer.get_prev())

if __name__ == '__main__':
	LD = LinkedDequeue()
	print("Enqueue:", end='')
	for x in range(0, 10):
	    LD.insert_first(x)
	    LD.insert_last(20-x)
	    print(x,20-x,end = ' ')
	print('')
	while not LD.is_empty():
	    print('first:%d last:%d' % (LD.delete_first(), LD.delete_last()))
