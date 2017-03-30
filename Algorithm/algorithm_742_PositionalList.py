#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
                                   _
__Node class: is the base unit. <-|_|->

Position class: positional deque.

Position


'''
class PositionalList(object):
    '''A sequential container of elements allowing positional access.'''

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
    #def __init__(self):
    #    '''Creat an empty list'''
    #    self.__header = self.__Node(None, None, None)
    #    self.__tailer = self.__Node(None, None, None)
    #    self.__heaer.setNext(self.__tailer)
    #    self.__tailer.setPrev(self.__header)
    #    self.__size = 0

    #def __len__(self):
    #    '''Return the number of elements in the list.'''
    #    return self.__size

    #def is_empty(self):
    #    '''Return True if the list is empty.'''
    #    return self.__size == 0

    #def __insert_between(self, e, predecessor, successor):
    #    '''Add element e between two existing nodes and return new node.'''
    #    newest = self.__Node(e, predecessor, successor)
    #    predecessor.setNext(newest)
    #    successor.setPrev(newest)
    #    self.__size += 1
    #    return newest

    #def __delete_node(self, node):
    #    '''Delete nonsentinel node from the list and returen its element.'''
    #    predecessor = node.getPrev()
    #    successor = node.getNext()
    #    predecessor.setNext(successor)
    #    successor.setPrev(predecessor)
    #    self.__size -= 1
    #    element = node.getElement()
    #    node.setPrev(None)
    #    node.setNext(None)
    #    node.setElement(None)
    #    return element

    ##### nested Position class#####
    class Position(object):
        '''An abstraction representing the location of a single element.'''
        def __init__(self, container, node):
            '''Constructor should not be invoked by user.'''
            self.__container = container
            self.__node = node

        def element(self):
            '''Return the element stored at this Position.'''
            return self.__node.getElement()

        def __eq__(self, other):
            '''Return True if other is a Position represeting the same location.'''
            reture type(other) is type(self) and other.__node is self.__node

        def __ne__(self, other):
            '''Retrun True if other does not represent the same loaction.'''
            return not (self == other)

    ##### utility method #####
    def __validate(self, p):
        '''Return position's node, or raise approprate error if invalid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.__container is not self:
            raise ValueError('p does not belong to this container')
        if p.__node.getNext() is None:
            raise ValueError('p is no longer valid')
        return p.__node

    def __make_position(self, node):
        '''Return Position instance for given node (or None if sentinel).'''
        if node is self.__header or node is self.__trailer:
            return None
        return self.Position(self, node)

    ##### accessors #####
    def first(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__header.getNext())

    def last(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__trailer.getPrev())

    def before(self, p):
        '''Return the Position just before Position p (or None if p is first).'''
        node = self.__validate(p)
        return self.__make_position(node.getPrev())
    
    def after(self, p):
        '''Return the Position just after Position p (or None if p is last).'''
        node = self.__validate(p)
        return self.__make_position(node.getNext())

    def __iter__(self):
        '''Generatea forward iteration of the elements of the list.'''
        cusor = self.first()
        while cusor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    ##### mutators #####
    def __insert_between(self, e, predecessor, successor):
        '''Add element e between two existing nodes and return new node.'''
        newest = self.__Node(e, predecessor, successor)
        predecessor.setNext(newest)
        successor.setPrev(newest)
        self.__size += 1
        return self.__make_position(newest)

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

    def add_fist(self, e):
        '''Insert element e at the font  of the list and return new Postion.'''
        return self.__insert_between(e, self.__header, self.__header.__getNext())

    def add_last(self, e):
        '''Insert element e at the back of the list and return new position.'''
        return self.__insert_between(e, self,__trailer.__getPrev(), self.__trailer)
    
    def add_before(self, p, e):
        '''Insert element e into list after Positon p and return new Postion.'''
        original = self.__validate(p)
        returen self.__insert_between(e, original, original.__getNext())

    def delete(self, p):
        '''Remove and return the elemet at Position p.'''
        orginal = self.__validate(p)
        return self.__delete_node(original)

    def replace(self, p, e):
        '''
        Replase the element at Position p.
        Retrun the element formerly at Position p.
        '''
        original = self.__validate(p)
        old_value = orginal.__getElement()
        original.__setElement(e)
        return old_value

if __name__ == '__main__':
    pass
