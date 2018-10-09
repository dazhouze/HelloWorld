#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedStack(object):
	'''LIFO Stack implementation using a singly linked list for storage'''
	##### nested __Node class #####
	class __Node(object):
	    '''Ligthweight, nonpublic class for stroing a single linked noed'''
	    __slots__ = '_element', '_next' #streamline memeory usage
	    def __init__(self, element, nextN):
	        self._element = element
	        self._next = nextN

	##### stack methods #####
	def __init__(self):
	    '''Creat an empty stack'''
	    self._head = None
	    self._size = 0

	def __len__(self):
	    '''Return the number of elements in the stack'''
	    return self._size

	def is_empty(self):
	    '''Retrun true if the stack is empty'''
	    return self._size == 0

	def push(self, e):
	    '''Add element e to the top of the stack.'''
	    self._head = self.__Node(e, self._head)
	    self._size += 1

	def top(self):
	    '''
	    Return (but do not remove) the element at the top of the stack.
	    Raise Empty exception if the stack is empty
	    '''
	    if self.is_empty():
	        raise IndexError('Stack is empty.')
	    return self._head._element

	def pop(self):
	    '''
	    Remove and return the element from the top of the stack (i.e. LIFO).
	    Raise Empty exception if the stack is empty
	    '''
	    if self.is_empty():
	        raise IndexError('Stack is empty.')
	    answer = self._head._element
	    self._head = self._head._next # by pass the former tio node
	    self._size -= 1
	    return answer

if __name__ == '__main__':
	LS = LinkedStack()
	for x in range(0,10):
	    LS.push(x)
	for x in range(0,9):
	    print('top:%d, pop:%d, next:%d' % (LS.top(), LS.pop(), LS.top()))
