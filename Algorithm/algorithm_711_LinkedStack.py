#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedStack(object):
    '''LIFO Stack implementation using a singly linked list for storage'''

    ##### nested __Node class #####
    class __Node(object):
        '''Ligthweight, nonpublic class for stroing a single linked noed'''
        __slots__ = '__element', '__next' #streamline memeory usage
        
        def __init__(self, element, nextN):
            self.__element = element
            self.__next = nextN

        def getElement(self):
            return self.__element
            
        def getNext(self):
            return self.__next

        def setElement(self, e):
            self.__element = e
        
        def setNext(self, n):
            self.__next = n
        
        
    ##### stack methods #####
    def __init__(self):
        '''Creat an empty stack'''
        self.__head = None
        self.__size = 0

    def __len__(self):
        '''Return the number of elements in the stack'''
        return self.__size

    def is__empty(self):
        '''Retrun true if the stack is empty'''
        return self.__size == 0

    def push(self, e):
        '''Add element e to the top of the stack.'''
        self.__head = self.__Node(e, self.__head)
        self.__size += 1

    def top(self):
        '''
        Return (but do not remove) the element at the top of the stack.
        Raise Empty exception if the stack is empty
        '''
        if self.is__empty():
            raise IndexError('Stack is empty.')
        return self.__head.getElement()

    def pop(self):
        '''
        Remove and return the element from the top of the stack (i.e. LIFO).
        Raise Empty exception if the stack is empty
        '''
        if self.is__empty():
            raise IndexError('Stack is empty.')
        answer = self.__head.getElement()
        self.__head = self.__head.getNext() # by pass the former tio node
        self.__size -= 1
        return answer

if __name__ == '__main__':
    LS = LinkedStack()
    for x in range(0,10):
        LS.push(x)
    for x in range(0,9):
        print('top:%d, pop:%d, next:%d' % (LS.top(), LS.pop(), LS.top()))
