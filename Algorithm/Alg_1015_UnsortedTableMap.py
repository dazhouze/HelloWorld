#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1014_MapBase import MapBase

class UnsortedTableMap(MapBase):
	'''Map implementation using an unoreded list.'''
	def __init__(self):
		'''Create an empty map.'''
		self._table = []
	
	def __getitem__(self, k):
		'''Return value associated with key k (raise KeyError if not found).'''
		for item in self._table:
			if k == item._key:
				return item._value
		raise KeyError('Key Error: ' + repr(k))

	def __setitem__(self, k, v):
		'''Assign value v to key k, overwritint existing value if present.'''
		for item in self._table:
			if k == item._key:
				item._value = v
				return
		self._table.append(self._Item(k, v))

	def __delitem__(self, k):
		'''Remove item associate with key k (raise KeyError if not found).'''
		for j in range(len(self._table)):
			if k == self._table[j]._key:
				self._table.pop(j)
				return
		raise KeyError('Key Error: ' + repr(k))

	def __len__(self):
		'''Return number of items in the map.'''
		return len(self._table)

	def  __iter__(self):
		'''Generate iteration of the map's keys.'''
		for item in self._table:
			yield item._key

if __name__ == '__main__':
	UTM = UnsortedTableMap()
	for x, y in zip((1,3,2), ('x','y','z')):
		UTM.setdefault(x, y)
	UTM[12] = 1
	print(len(UTM))
	del UTM[12]
	for x,y in sorted(UTM.items()):
		print(x, y)
