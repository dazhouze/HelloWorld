#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SortedPriorityQueue(object):
    ''' A min-oriented priority queue implemented with an un sorted list.'''

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

    def __init__(self):
        '''Creat a new empty Priority Queue.'''
        self.__data = PositionalList()

    def __len__(self):
        '''Return the number of items in the priority queue.'''
        return len(self.__data)

    def is_empty(self):
        '''Return True if the priority queue is empyt'''
        return len(self.__data) == 0

    def add(self, key, value):
        '''Add a key-value pair.'''
        newest = self._Item(key, value)
        walk = self.__data.last()
        while walk is not None and newest < walk.get_element():
            walk = self.__data.before(walk)
        if walk is None:
            self.__data.add_first(newest)
        else:
            self.__data.add_after(walk, newest)

    def min(self):
        '''Return but do not remeve (k, v) tuple with minimum key.'''
        if self.is_empty is not None:
            p = self.__data.first()
            item = p.get_element()
            return (item.get_key(), item.get_value())
        raise Empty('Priority queue is empty.')

    def remove_min(self):
        '''Remove and return (k, v) tuple with minmum key.'''
        if self.is_empty is not None:
            item = self.__data.delete(self.__data.first())
            return (item.get_key(), item.get_value())
        raise Empty('Priority queue is empty.')

class PositionalList(object):
    '''A sequential container of elements allowing positional access.'''

    class Position(object):
        '''An abstraction representing the location of a single element.'''
        def __init__(self, container, node):
            '''Constructor should not be invoked by user.'''
            self.__container = container # instance of PositionList class
            self.__node = node # instance of _Node class
            
        def get_container(self):
            return self.__container

        def get_node(self):
            return self.__node

        def get_element(self):
            '''Return the element stored at this Position.'''
            return self.get_node().get_element()

        def __eq__(self, other):
            '''Return True if other is a Position represeting the same location.'''
            return type(other) is type(self) and other.get_node() is self.get_node()

        def __ne__(self, other):
            '''Retrun True if other does not represent the same loaction.'''
            return not (self == other)

    def __validate(self, p):
        '''Return position's node, or raise approprate error if invalid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.get_container() is not self:
            raise ValueError('p does not belong to this container')
        if p.get_node().get_next() is None:
            raise ValueError('p is no longer valid')
        return p.get_node()

    def __make_position(self, node):
        '''Return Position instance for given node (or None if sentinel).'''
        if node is self.__header or node is self.__trailer:
            return None
        return self.Position(self, node)

    class _Node(object):
        '''Lightweigth, nonpublic class for storing a double linked node.'''
        __slots__ = '__element', '__prev', '__next'

        def __init__(self, e, p, n):
            self.__element = e
            self.__prev = p
            self.__next = n

        def get_prev(self):
            return self.__prev

        def get_next(self):
            return self.__next

        def get_element(self):
            return self.__element

        def set_prev(self, p):
            self.__prev = p

        def set_next(self, n):
            self.__next = n

        def set_element(self, e):
            self.__element = e

    def __init__(self):
        '''Creat an empty list'''
        self.__header = self._Node(None, None, None)
        self.__trailer = self._Node(None, None, None)
        self.__header.set_next(self.__trailer)
        self.__trailer.set_prev(self.__header)
        self.__size = 0

    def __len__(self):
        '''Return the number of elements in the list.'''
        return self.__size

    def is_empty(self):
        '''Return True if the list is empty.'''
        return self.__size == 0

    def first(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__header.get_next())

    def last(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__trailer.get_prev())

    def before(self, p):
        '''Return the Position just before Position p (or None if p is first).'''
        node = self.__validate(p)
        return self.__make_position(node.get_prev())
    
    def after(self, p):
        '''Return the Position just after Position p (or None if p is last).'''
        node = self.__validate(p)
        return self.__make_position(node.get_next())

    def __iter__(self):
        '''Generatea forward iteration of the elements of the list.'''
        cursor = self.first()
        while cursor is not None:
            yield cursor.get_element()
            cursor = self.after(cursor)

    ##### mutators #####
    def __insert_between(self, e, predecessor, successor):
        '''Add element e between two existing nodes and return new node.'''
        newest = self._Node(e, predecessor, successor)
        predecessor.set_next(newest)
        successor.set_prev(newest)
        self.__size += 1
        return self.__make_position(newest)

    def __delete_node(self, node):
        '''Delete nonsentinel node from the list and returen its element.'''
        predecessor = node.get_prev()
        successor = node.get_next()
        predecessor.set_next(successor)
        successor.set_prev(predecessor)
        self.__size -= 1
        element = node.get_element()
        node.set_prev(None)
        node.set_next(None)
        node.set_element(None)
        return element

    def add_first(self, e):
        '''Insert element e at the font  of the list and return new Postion.'''
        return self.__insert_between(e, self.__header, self.__header.get_next())

    def add_last(self, e):
        '''Insert element e at the back of the list and return new position.'''
        return self.__insert_between(e, self.__trailer.get_prev(), self.__trailer)
    
    def add_before(self, p, e):
        '''Insert element e into list after Positon p and return new Postion.'''
        original = self.__validate(p)
        return self.__insert_between(e, original.get_prev(), original)

    def add_after(self, p, e):
        '''Insert element e into list after Position pand return new Position.'''
        original = self.__validate(p)
        return self.__insert_between(e, original, original.get_next())

    def delete(self, p):
        '''Remove and return the elemet at Position p.'''
        original = self.__validate(p)
        return self.__delete_node(original)

    def replace(self, p, e):
        '''
        Replase the element at Position p.
        Retrun the element formerly at Position p.
        '''
        original = self.__validate(p)
        old_value = orginal.get_element()
        original.set_element(e)
        return old_value

if __name__ == '__main__':
    SL = SortedPriorityQueue()
    SL.add(1, 11)
    SL.add(3, 13)
    SL.add(5, 15)
    SL.add(1, 12)
    print(SL.min())
    print(SL.remove_min())
    print(SL.min())
