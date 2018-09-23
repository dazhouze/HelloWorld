#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ArrayQueue(object):
    '''FIFO queue implementation using a Python list as underlying storages.'''
    DEFAULT_CAPACITY = 10 # moderate for all new queues

    def __init__(self):
        '''Create an empty queue'''
        self.__data = [None] * ArrayQueue.DEFAULT_CAPACITY # constant in class need to be annoanced
        self.__size = 0
        self.__front = 0

    def __len__(self):
        '''Retrun the number of elemetns in the queue'''
        return self.__size

    def is_empty(self):
        '''Return True if the queue is empty'''
        return self.__size == 0

    def first(self):
        '''
        Return (but do not remove) the element at the front of the queue
        Raise Empty excepython if the queue is empty
        '''
        if self.is_empty():
            raise IndexError('Queue is empty.')
        return self.__data[self.__front]

    def dequeue(self):
        '''
        Remove and return the first element of the queue
        Raise Empty excepyion if the queue is empty
        '''
        if self.is_empty():
            raise IndexError('Queue is empty.')
        answer = self.__data[self.__front]
        self.__data[self.__front] = None
        self.__front = (self.__front+1)%len(self.__data)
        self.__size -= 1
        '''shrringking the underlying array'''
        if 0 < self._size< len(self.__data)//4:
                self.__resize(len(self.__data)//2)
        return answer

    def enqueue(self, e):
        '''Add an element to the back of queue'''
        if self.__size == len(self.__data):
            self.__resize(2*self.__size)
        avail = (self.__front + self.__size) % len(self.__data)
        self.__data[avail] = e
        self.__size += 1

    def __resize(self, cap):
        '''Resize to a new list of capaciyt'''
        old = self.__data
        self.__data = [None] * cap
        walk = self.__front
        for k in range(0, self.__size):
            self.__data[k] = old[walk]
            walk = (1+walk) % len(old)
        self.__front = 0


if __name__ == '__main__':
    AQ = ArrayQueue()
    for i in range(19):
        AQ.enqueue(i)
        print("enqueue:%d, size:%d"%(i,len(AQ)))
    for i in range(18,0,-1):
        print('first: %d dequeue: %d, next: %d'%(AQ.first(), AQ.dequeue(), AQ.first()))
