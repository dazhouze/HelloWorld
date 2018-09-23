#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class HeapPriorityQueue(object):
    ''' A min-oriented priority queue implemented with a binary heap.'''
    class _Item(object):
        '''Lightweight composite to store priority queue items.'''
        __slots__ = '__key', '__value'

        def __init__(self, k, v):
            self.__key = k
            self.__value = v

        def __lt__(self, other):
            '''Redefine __lt__ to compare 2 _Item instance based on __key'''
            return self.__key < other.__key

        def get_key(self):
            '''Return key of _Item'''
            return self.__key

        def get_value(self):
            '''Return value of _Item'''
            return self.__value

    def __init__(self, contents=()):
        '''Creat a new empty Priority Queue.
        By default, queue will be empty. If contents is given, it should be as an
        iterable sequence of (k, v) tuples specifying the initial contents.
        '''
        self.__data = [self._Item(k, v) for k, v in contents]
        if len(self.__data) > 1:
            self.__heapify()

    def __heapify(self):
        start = self.__parent(len(self) - 1)
        for j in range(start, -1, -1):
            self.__downheap(j)

    def __len__(self):
        '''Return the number of items in the priority queue.'''
        return len(self.__data)

    def is_empty(self):
        '''Return True if the priority queue is empyt'''
        return len(self.__data) == 0

    def __parent(self, j):
        return (j-1)//2

    def __left(self, j):
        return 2*j + 1

    def __right(self, j):
        return 2*j + 2
    
    def __has_left(self, j):
        return self.__left(j) < len(self.__data)

    def __has_right(self, j):
        return self.__right(j) < len(self.__data)

    def __swap(self, i, j):
        '''Swap the element at indices i and j of array.'''
        self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

    def __upheap(self, j):
        '''When add _Item.'''
        parent = self.__parent(j)
        if j > 0 and self.__data[j] < self.__data[parent]:
            self.__swap(j, parent)
            self.__upheap(parent)

    def __downheap(self, j):
        '''When rm min _Item.'''
        if self.__has_left(j):
            left = self.__left(j)
            small_child = left
            if self.__has_right(j):
                right = self.__right(j)
                if self.__data[right] < self.__data[left]:
                    small_child = right
            if self.__data[small_child] < self.__data[j]:
                self.__swap(j, small_child)
                self.__downheap(small_child)

    def add(self, key, value):
        '''Add a key-value pair to the priority queue.'''
        self.__data.append(self._Item(key, value))
        self.__upheap(len(self.__data) - 1)

    def min(self):
        '''Return but do not remove (k, v) tuple with minimum key.
        Raise Empth exception if empty.
        '''
        if self.is_empty():
            raise ValueError('Priority queue is empty.')
        item = self.__data[0]
        return (item.get_key(), item.get_value())

    def remove_min(self):
        '''Remove and return (k, v) tuple with minimum key.
        Raise ValueError exceptio if empty.
        '''
        if self.is_empty():
            raise ValueError('Priority queue is empty.')
        self.__swap(0, len(self.__data) - 1)
        item = self.__data.pop()
        self.__downheap(0)
        return (item.get_key(), item.get_value())

if __name__ == '__main__':
    HPQ = HeapPriorityQueue()
    HPQ.add(1, 11)
    HPQ.add(3, 13)
    HPQ.add(5, 15)
    HPQ.add(1, 12)
    print(len(HPQ))
    print(HPQ.min())
    print(HPQ.remove_min())
    print(HPQ.min())
