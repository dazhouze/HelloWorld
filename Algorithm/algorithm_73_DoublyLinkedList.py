#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class __DoublyLinkedBase(object):
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
        self.__tailer = self.__Node(None, None, None)
        self.__heaer.setNext(self.__tailer)
        self.__tailer.setPrev(self.__header)
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

if __name__ == '__main__':
    pass
