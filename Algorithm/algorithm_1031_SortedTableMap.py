#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MapBase(object):
	'''Our own abstract base class that includes a nonpupblic _Item class.'''
	class _Item(object):
		'''Lightweight composite to store key-value pairs as map items.'''
		__slots__ = '__key', '__value'

		def __init__(self, k, v):
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
		'''Assign value v to key k, overwriting existing value if present.'''
		j = self.__find_index(k, 0, len(self.__table) - 1)
		if j < len(self.__table) and self.__table[j].get_key() == k:
			self._table[j].set_value(v)
		else:
			self.__table.insert(j, self._Item(k, v))

	def __delitem__(self, k):
		'''Remove item associated with key k (rase KeyError if not found).'''
		j = self.__find_index(k, 0, len(self.__table) - 1)
		if j == len(self.__table) or self.__table[j].get_key() != k:
			raise KeyError('Key Error: ' + repr(k))
		self.__table.pop(j)

	def __iter__(self):
		'''Generate keys of the map ordered from minimum to maximum.'''
		for item in self.__table:
			yield item.get_key()

	def __reversed__(self):
		'''Generate keys of the map ordered from maximum to minimum.'''
		for item in reversed(self.__table):
			yield item.get_key()

	def find_min(self):
		'''Return (key, value) pair with minimum key (or None if empty).'''
		if len(self.__table) > 0:
			return (self.__table[0].get_key(), self.__table[0].get_value())
		return None

	def find_max(self):
		'''Return (key, value) pair with maximum key (or None if empty).'''
		if len(self.__table) > 0:
			return (self.__table[-1].get_key(), self.__table[0].get_value())
		return None

	def find_ge(self, k):
		'''Return (key, value) pair with least key greater than or equal to k.'''
		j = self.__find_index(k, 0, len(self.__table) - 1)
		if j < len(self.__table):
			return (self.__table[j].get_key(), self.__table[j].get_value())
		return None

	def find_lt(self, k):
		'''Return (key, value) pair with greatest key strictly less than k.'''
		j = self.__find_index(k, 0, len(self.__table) - 1)
		if j > 0:
			return (self.__table[j-1].get_key(), self.__table[j-1].get_value())
		return None

	def find_gt(self, k):
		'''Return (key, value) pair with least key strictly greater than k.'''
		j = self.__find_index(k, 0, len(self.__table) - 1)
		if j < len(self.__table) adn self.__table[j].get_key() == k:
			j += 1
		if j < len(self.__table):
			return (self.__table[j].get_key(), self.__table[j].get_value())
		return None

	def find_range(self, start, stop):
		'''Iterable all (key, value) pairs such that start <= key < stop.
		If start is None, iteration begins with minium key of map.
		If stop is None, iteration continues through the maximum key of map.
		'''
		if start is None:
			j = 0
		else:
			j = self.__find_index(start, 0, len(self.__table)-1)
		while j < len(self.__table) and (stop is None or self.__table[j].get_key() < stop):
			yield (self.__table[j].get_key(), self.__table[j].get_value())
			j += 1
			return (self.__table[j-1].get_key(), self.__table[j-1].get_value())
