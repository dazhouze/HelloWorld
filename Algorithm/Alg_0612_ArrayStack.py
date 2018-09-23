#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class ArrayStack(object):
	'''LIFO Stack implementation using a Pyhotn list as underlying storage'''
	def __init__(self):
	    '''Creat an empty stack'''
	    self.__data = [None] # nonpublic list instance

	def __len__(self):
	    '''Return the number of elements in the stack'''
	    return len(self.__data)

	def is_empty(self):
	    '''Return True if the stack is empty'''
	    return len(self.__data) == 0

	def push(self, e):
	    '''Add elements to the top of the stack'''
	    self.__data.append(e)

	def top(self):
	    '''
	    Return (but do not remove) the element at the top of the stack
	    Raise Empty exception if the stack is empty
	    '''
	    try:
	        return self.__data[-1]
	    except :
	        raise IndexError('Stack is empty.')
	
	def pop(self):
	    '''
	    Remove and return the element from the tio of stack.
	    Raise Empty exception
	    '''
	    try:
	        return self.__data.pop()
	    except:
	        raise IndexError('Stack is empty.')




if __name__ == '__main__':
	Ay = ArrayStack()
	Ay.push(3)
	Ay.push(4)
	Ay.push(5)
	print(Ay)
	print(Ay.pop())
	print(Ay.pop())
	print(Ay.top())
	print(Ay.top())
