#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0742_PositionalList import PositionalList

'''
FavoritesList: based on PositionalList()
	_Item(): value and count
	__init__(): PositionalList()
	__len__:
	is_empty:
	access(): _Item.value
	top():
	remove():
	_find_position(): fine target element in PositionalList
	_move_up():
	
'''

class FavoritesList(object):
	'''List of elementsordered from most frequently accessed to least.'''
	##### nested _Item class #####
	class _Item(object):
		__slots__ = '__value', '__count'
		def __init__(self,e):
			self.__value = e
			self.__count = 0

		def getValue(self):
			'''Return the value of _Item.'''
			return self.__value

		def getCount(self):
			'''Return the count of _Item.'''
			return self.__count

		def addCount(self):
			'''Add 1 to the count of _Item.'''
			self.__count += 1

	##### nonpublic utilities of class FavoritesList #####
	def _find_position(self, e):
		'''Search for element e and return its Position (or None if not found).'''
		walk = self._data.first()
		while walk is not None and walk.get_element().getValue() != e:
			walk = self._data.after(walk)
		return walk

	def _move_up(self, p):
		'''Move item at Postion p earlier in the list based on access count.'''
		if p != self._data.first():
			cnt = p.get_element().getCount()
			walk = self._data.before(p)
			if cnt > walk.get_element().getCount():
				while walk!=self._data.first() and cnt>self._data.before(walk).get_element().getCount():
					walk = self.__dat.before(walk)
				self._data.add_before(walk, self._data.delete(p))

	##### public utilities of class FavoritesList #####
	def __init__(self):
		'''Create an empty list of favorites.'''
		self._data = PositionalList() # init a positional list
	
	def __len__(self):
		'''Return number of entries on favorites list.'''
		return len(self._data)

	def is_empty(self):
		'''Retrun True if the list is empty.'''
		return len(self._data)==0

	def access(self, e):
		'''Access element e, thereby increasing its access count.'''
		p = self._find_position(e) # try to locate existing element
		if p is None:
			p = self._data.add_last(self._Item(e))
		p.get_element().addCount() # count += 1
		self._move_up(p)

	def remove(self, e):
		'''Remove element e frome the list of favorites.'''
		p = self._find_position(e)
		if p is not None:
			self,_data.delete(p)

	def top(self, k):
		'''Generate sequence of topk elements in terms of access count.'''
		if not 1<= k <= len(self):
			raise ValueError('Illegal value for k.')
		walk = self._data.first()
		for j in range(0, k):
			item = walk.get_element()
			yield item.getValue()
			walk = self._data.after(walk)

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
