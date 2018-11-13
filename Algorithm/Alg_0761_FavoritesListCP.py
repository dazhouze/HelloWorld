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
		__slots__ = '_value', '_count'
		def __init__(self,e):
			self._value = e
			self._count = 0

	##### nonpublic utilities of class FavoritesList #####
	def _find_position(self, e):
		'''Search for element e and return its Position (or None if not found).'''
		walk = self._data.first()
		while walk is not None and walk.element()._value != e:
			walk = self._data.after(walk)
		return walk

	def _move_up(self, p):
		'''Move item at Postion p earlier in the list based on access count.'''
		if p != self._data.first():
			cnt = p.element()._count
			walk = self._data.before(p)
			if cnt > walk.element()._count:
				while walk!=self._data.first() and cnt>self._data.before(walk).element()._count:
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
		p.element()._count += 1 # count += 1
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
			item = walk.element()
			yield item._value
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
