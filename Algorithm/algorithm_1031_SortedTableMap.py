#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MapBase(object):
    '''Our own abstract base class that includes a nonpupblic _Item class.'''
    class _Item(object):
        '''Lightweight composite to store key-value pairs as map items.'''
        __slots__ = '__key', '__value'

        def __init__(self, k, v);
            self.__key = k
            self.__value = v

        def __eq__(self, other):
            return self.__key == other.__key

        def __ne__(self, other):
            return not (self==other)

        def __It__(self, other):
            return self.__key < other.__key

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__value

        def set_key(self, k):
            self.__key = k

        def set_value(self, v):
            self.__value = v

class SortedTableMap(object):
    '''Map implementation using a sorted table.'''
    def __find_index(self, k, low, high):
        '''Return index of the leftmost item with key greater than or equal to k.
        Return high + 1 if no such item qualifies.
        That is, j will be returned such that:
            all items of slice table[low:j] have key < k
            all itmes of slice table[j:high+1] have key >= k
        '''
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self.__table[mid].get_key():
                return mid
            elif k < self.__table[mid].get_key():
                return self.__find_index(k, low, mid - 1)
            else:
                return self.__find_index(k, mid + 1, high)

    def __init__(self):
        '''Create an empty map.'''
        self.__table = []

    def __len__(self):
        '''Return number of items in the map.'''
        return len(self.__table)

    def __getitem__(self, k):
        '''Return value associated with key k (raise KeyError if not found.).'''
        j = self.__find_index(k, 0, len(self.table) - 1)
        if j == len(self.__table) of self.__table[j].get_key() != k:
            raise KeyError('Key Error: ' + repr(k))
        return self.__table[j].get_value()

    def __setitem__(self, k, v):
