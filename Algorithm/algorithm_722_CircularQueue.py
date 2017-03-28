#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class CircularQueue(object):
    '''Queue implementation using a circular linked list for storage'''

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

        def setNext(self, n):
            self.__next = n
        
    ##### queue methods #####
    def __init__(self):
        '''Creat an empty queue'''
        self.__tail = None
        self.__size = 0

    def __len__(self):
        '''Return the number of elements in the queue'''
        return self.__size

    def is_empty(self):
        '''Retrun true if the queue is empty'''
        return self.__size == 0

    def first(self):
        '''Retrun (but do not remove) the element at the front of the queue'''
        if self.is_empty():
            raise IndexError('Queue is empty.')
        head = self.__tail.getNext()
        return head.getElement()

    def dequeue(self):
        '''
        Remove and retrun the first element of the queue (i.e. FIFO).
        Raise Empty exception if the queue is empty.
        '''
        if self.is_empty():
            raise IndexError('Queue is empty.')
        oldHead = self.__tail.getNext()
        if self.__size == 1:
            self.__tail = None
        else:
            self.__tail.setNext(oldHead.getNext())
        self.__size -= 1
        return oldHead.getElement()

    def enqueue(self, e):
        '''Add an element to the back of queue'''
        newest = self.__Node(e, None)
        if self.is_empty():
            newest.setNext(newest)
        else:
            newest.setNext(self.__tail.getNext())
            self.__tail.setNext(newest)
        self.__tail = newest
        self.__size += 1

    def rotate(self):
        '''Rotate front element to the back of queue'''
        if self.__size > 0:
            self.__tail = self.__tail.getNext()

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
