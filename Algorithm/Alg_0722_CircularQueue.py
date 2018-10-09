#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class CircularQueue(object):
	'''Queue implementation using a circular linked list for storage'''
	##### nested _Node class #####
	class _Node(object):
	    '''Ligthweight, nonpublic class for stroing a single linked noed'''
	    __slots__ = '_element', '_next' #streamline memeory usage
	    
	    def __init__(self, element, nextN):
	        self._element = element
	        self._next = nextN

	##### queue methods #####
	def __init__(self):
	    '''Creat an empty queue'''
	    self._tail = None
	    self._size = 0

	def __len__(self):
	    '''Return the number of elements in the queue'''
	    return self._size

	def is_empty(self):
	    '''Retrun true if the queue is empty'''
	    return self._size == 0

	def first(self):
	    '''Retrun (but do not remove) the element at the front of the queue'''
	    if self.is_empty():
	        raise IndexError('Queue is empty.')
	    head = self._tail._next
	    return head._element

	def dequeue(self):
	    '''
	    Remove and retrun the first element of the queue (i.e. FIFO).
	    Raise Empty exception if the queue is empty.
	    '''
	    if self.is_empty():
	        raise IndexError('Queue is empty.')
	    oldHead = self._tail._next
	    if self._size == 1:
	        self._tail = None
	    else:
	        self._tail._next = oldHead._next
	    self._size -= 1
	    return oldHead._element

	def enqueue(self, e):
	    '''Add an element to the back of queue'''
	    newest = self._Node(e, None)
	    if self.is_empty():
	        newest._next = newest
	    else:
	        newest._next = self._tail._next
	        self._tail._next = newest
	    self._tail = newest
	    self._size += 1

	def rotate(self):
	    '''Rotate front element to the back of queue'''
	    if self._size > 0:
	        self._tail = self._tail._next

if __name__ == '__main__':
	SQ = CircularQueue()
	print('enqueue: ', end='')
	for x in range(0,10):
	    SQ.enqueue(x)
	    print(x, end='')
	print('')
	SQ.rotate()
	for x in range(0,9):
	    print('first:%d, dequeue:%d, after:%d' % (SQ.first(), SQ.dequeue(), SQ.first()))
