#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class AdaptableHeapPriorityQueue(object):
    '''A locator-based priority queue implemented with a binary heap.'''
    class Locator(object):
        '''Token for locating an entry of the priority queue.'''
        __slots__ = '__key', '__value', '__index'

        def __init__(self, k, v, j):
            self.__key = k
            self.__value = v
            self.__index = j

        def __lt__(self, other):
            '''Redefine __lt__ to compare 2 _Item instance based on __key'''
            return self.__key < other.__key

        def get_key(self):
            '''Return key of _Item'''
            return self.__key

        def get_value(self):
            '''Return value of _Item'''
            return self.__value

        def get_index(self):
            '''Return index of _Item'''
            return self.__index

        def set_index(self, i):
            '''Set index of _Item'''
            self.__index = i

        def set_key(self, k):
            '''Set key of _Item'''
            self.__key = k

        def set_value(self, v):
            '''Set value of _Item'''
            self.__value = v

    def __init__(self):
        '''Creat a new empty Priority Queue.'''
        self.__data = []

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
        self.__data[i].set_index(i)
        self.__data[j].set_index(j)

    def __bubble(self,j):
        if j > 0 and self.__data[j] < self.__data[self.__parent(j)]:
            sefl.__upheap(j)
        else:
            self.__downheap(j)
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
        token = self.Locator(key, value, len(self.__data))
        self.__data.append(token)
        self.__upheap(len(self.__data) - 1)
        return token

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

    def update(self, loc, new_key, new_val):
        '''Update the key and value for the entry indextified by Locator loc.'''
        j = loc.get_index()
        if not (0 <= j < len(self) and self.__data[j] is loc):
            raise ValueError('Invalid locator')
        loc.set_key(new_key)
        loc.set_value(new_val)
        self.__bubble(j)

    def remove(self, loc):
        '''Remove and return the (k, v) pair identified by Locator loc.'''
        j = loc.get_index()
        if not (0 <= j < len(self) and self.__data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:
            self.__data.pop()
        else:
            self.__swap(j, len(self) - 1)
            self.__data.pop()
            self.__bubble(j)
        return (loc.get_key(), loc.get_value())
if __name__ == '__main__':
    AHPQ = AdaptableHeapPriorityQueue()
    AHPQ.add(1, 11)
    AHPQ.add(3, 13)
    AHPQ.add(5, 15)
    AHPQ.add(1, 12)
    print(len(AHPQ))
    print(AHPQ.min())
    print(AHPQ.remove_min())
    print(AHPQ.min())
