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

