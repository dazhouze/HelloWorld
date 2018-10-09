#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0742_PositionalList import PositionalList

'''
FavoritesList: based on PositionalList()
	__Item(): value and count
	__init__(): PositionalList()
	__len__:
	is_empty:
	access(): __Item.value
	top():
	remove():
	__find_position(): fine target element in PositionalList
	__move_up():
	
'''

class FavoritesList(object):
	'''List of elementsordered from most frequently accessed to least.'''
	##### nested __Item class #####
	class __Item(object):
	    __slots__ = '__value', '__count'
	    def __init__(self,e):
	        self.__value = e
	        self.__count = 0

	    def getValue(self):
	        '''Return the value of __Item.'''
	        return self.__value

	    def getCount(self):
	        '''Return the count of __Item.'''
	        return self.__count

	    def addCount(self):
	        '''Add 1 to the count of __Item.'''
	        self.__count += 1

	##### nonpublic utilities of class FavoritesList #####
	def __find_position(self, e):
	    '''Search for element e and return its Position (or None if not found).'''
	    walk = self.__data.first()
	    while walk is not None and walk.element().getValue() != e:
	        walk = self.__data.after(walk)
	    return walk

	def __move_up(self, p):
	    '''Move item at Postion p earlier in the list based on access count.'''
	    if p != self.__data.first():
	        cnt = p.element().getCount()
	        walk = self.__data.before(p)
	        if cnt > walk.element().getCount():
	            while walk!=self.__data.first() and cnt>self.__data.before(walk).element().getCount():
	                walk = self.__dat.before(walk)
	            self.__data.add_before(walk, self.__data.delete(p))

	##### public utilities of class FavoritesList #####
	def __init__(self):
	    '''Create an empty list of favorites.'''
	    self.__data = PositionalList() #
	
	def __len__(self):
	    '''Return number of entries on favorites list.'''
	    return len(self.__data)

	def is_empty(self):
	    '''Retrun True if the list is empty.'''
	    return len(self.__data)==0

	def access(self, e):
	    '''Access element e, thereby increasing its access count.'''
	    p = self.__find_position(e) # try to locate existing element
	    if p is None:
	        p = self.__data.add_last(self.__Item(e))
	    p.element().addCount() # count += 1
	    self.__move_up(p)

	def remove(self, e):
	    '''Remove element e frome the list of favorites.'''
	    p = self.__find_position(e)
	    if p is not None:
	        self,__data.delete(p)

	def top(self, k):
	    '''Generate sequence of topk elements in terms of access count.'''
	    if not 1<= k <= len(self):
	        raise ValueError('Illegal value for k.')
	    walk = self.__data.first()
	    for j in range(0, k):
	        item = walk.element()
	        yield item.getValue()
	        walk = self.__data.after(walk)

if __name__ == '__main__':
	FL = FavoritesList()
	FL.access(1)
	FL.access(2)
	FL.access(2)
	FL.access(3)
	FL.access(3)
	FL.access(3)
	top = FL.top(3)
	for x in range(0,3):
	    print(next(top))
