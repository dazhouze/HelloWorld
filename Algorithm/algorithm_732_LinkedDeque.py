#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedDequeue(object):
    '''A base class providing a doubly linked list representation.'''

    ##### __Node class #####
    class __Node(object):
        '''Lightweigth, nonpublic class for storing a double linked node.'''
        __slots__ = '__element', '__prev', '__next'

        def __init__(self, e, p, n):
            self.__element = e
            self.__prev = p
            self.__next = n

        def getPrev(self):
            return self.__prev

        def getNext(self):
            return self.__next

        def getElement(self):
            return self.__element

        def setPrev(self, p):
            self.__prev = p

        def setNext(self, n):
            self.__next = n

        def setElement(self, e):
            self.__element = e

    ##### doubly linked base class and method #####
    def __init__(self):
        '''Creat an empty list'''
        self.__header = self.__Node(None, None, None)
        self.__trailer = self.__Node(None, None, None)
        self.__header.setNext(self.__trailer)
        self.__trailer.setPrev(self.__header)
        self.__size = 0

    def __len__(self):
        '''Return the number of elements in the list.'''
        return self.__size

    def is_empty(self):
        '''Return True if the list is empty.'''
        return self.__size == 0

    def __insert_between(self, e, predecessor, successor):
        '''Add element e between two existing nodes and return new node.'''
        newest = self.__Node(e, predecessor, successor)
        predecessor.setNext(newest)
        successor.setPrev(newest)
        self.__size += 1
        return newest

    def __delete_node(self, node):
        '''Delete nonsentinel node from the list and returen its element.'''
        predecessor = node.getPrev()
        successor = node.getNext()
        predecessor.setNext(successor)
        successor.setPrev(predecessor)
        self.__size -= 1
        element = node.getElement()
        node.setPrev(None)
        node.setNext(None)
        node.setElement(None)
        return element

    def first(self):
        '''Return (but do not remove) the element at the front of the deque.'''
        if self.is_empty():
            raise IndexError('Deque is empty')
        return self.__header.getNext().getElement()

    def last(self):
        '''Return (but do not remove) the element at the back of the deque.'''
        if self.is_empty():
            raise IndexError('Deque is empty.')
        return self.__trailer.getPrev().getElement()

    def insert_first(self, e):
        '''Add an element to the front of the deque.'''
        self.__insert_between(e, self.__header, self.__header.getNext())

    def insert_last(self, e):
        '''Add an element to the back of the deque.'''
        self.__insert_between(e, self.__trailer.getPrev(), self.__trailer)

    def delete_first(self):
        '''
        Remove and return the element from the front of the deque.
        Raise Empty exception if the deque is empty.
        '''
        if self.is_empty():
            raise IndexError('Deque is empty.')
        return self.__delete_node(self.__header.getNext())

    def delete_last(self):
        '''
        Remove and return the element from the back of the deque.
        Raise Empty exception if the deque is empty.
        '''
        if self.is_empty():
            raise IndexError('Deque is empty.')
        return self.__delete_node(self.__trailer.getPrev())

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
