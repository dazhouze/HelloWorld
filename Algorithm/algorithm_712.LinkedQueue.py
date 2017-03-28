#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedQueue:
    '''FIFO Queue implementation using a singly linked list for storage'''

    ##### nested __Node class #####
    class __Node:
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
        
    ##### queue methods #####
    def __init__(self):
        '''Creat an empty queue'''
        self.__head = None
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
        return self.__head.getElement()

    def dequeue(self):
        '''
        Remove and retrun the first element of the queue (i.e. FIFO).
        Raise Empty exception if the queue is empty.
        '''
        if self.is_empty():
            raise IndexError('Queue is empty.')
        answer = self.__head.getElement()
        self.__head = self.__head.getNext()
        self.__size -= 1
        if self.is_empty(): # check after dequeue
            self.__tail = None
        return answer

    def enqueue(self, e):
        '''Add an element to the back of queue'''
        newest = self.__Node(e, None)
        if self.is_empty():
            self.__head = newest
        else:
            self.__tail.setNext(newest)
        self.__tail = newest
        self.__size += 1

if __name__ == '__main__':
    LQ = LinkedQueue()
    print('enqueue: ', end='')
    for x in range(0,10):
        LQ.enqueue(x)
        print(x, end='')
    print('')
    for x in range(0,9):
        print('first:%d, dequeue:%d, after:%d' % (LQ.first(), LQ.dequeue(), LQ.first()))
