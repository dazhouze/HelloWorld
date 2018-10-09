#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class ArrayStack(object):
	'''LIFO Stack implementation using a Pyhotn list as underlying storage'''
	def __init__(self):
		'''Creat an empty stack'''
		self._data = [] # nonpublic list instance

	def __len__(self):
		'''Return the number of elements in the stack'''
		return len(self._data)

	def is_empty(self):
		'''Return True if the stack is empty'''
		return len(self._data) == 0

	def push(self, e):
		'''Add elements to the top of the stack'''
		self._data.append(e)

	def top(self):
		'''
		Return (but do not remove) the element at the top of the stack
		Raise Empty exception if the stack is empty
		'''
		try:
			return self._data[-1]
		except :
			raise IndexError('Stack is empty.')
	
	def pop(self):
		'''
		Remove and return the element from the tio of stack.
		Raise Empty exception
		'''
		try:
			return self._data.pop()
		except:
			raise IndexError('Stack is empty.')

if __name__ == '__main__':
	ay = ArrayStack()
	print(ay.is_empty())
	ay.push(3)
	ay.push(4)
	ay.push(5)
	print(ay)
	while ay:
		print(ay.top())
		print(ay.pop())
