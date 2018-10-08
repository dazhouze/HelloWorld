#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Two implementations of a hash table,
one using separate chaining 
and the other using open addressing with linear probing. 
'''

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

class HashMapBase(MapBase):
	'''Abstract base class for map using hash-table with MAD compression.'''
	def __init__(self, cap=11, p=109345121):
		'''Create an empty hash-table map.'''
		self.__table = cap * [None]
		self.__n = 0
		self.__prime = p
		self.__scale = 1 + randrange(p-1)
		self.__shift = randrange(p)

	def __hash_function(self, k):
		return (hash(k)*self.__scale + self.__shift) % self.__prime % len(self.__table)

	def __len__(self):
		return self.__n

	def __getitem__(self, k):
		j = self.__hash_function(k)
		return self.__bucket_getitem(j, k)

	def __setitem__(self, k, v):
		j = self.__hash_function(k)
		self,__bucket_setitem(j, k, v)
		if self.__n > len(self.__table) // 2:
			self.__resize(2 * len(self.__table - 1))

	def __delitem__(self, k):
		j = self.__hash_function(k)
		self.__bucket_delitem(j, k)
		self.__n -= 1

	def __resize(self, c):
		old = list(self.items())
		self.__table = c * [None]
		self.__n = 0
		for (k, v) in old:
			self[k] = v

class ChainHashMap(HashMapBase):
	'''Hash map implemented with separate chaining for collision resolution.'''
	def __bucket_getitem(self, j, k):
		bucket = self.__table[j]
		if bucket is None:
			raise KeyError('Key Error: ' + repr(k))
		return bucket[k]

	def __bucket_setitem(self, j, k, v):
		if self.__table[j] is None:
			self.__table[j] = UnsortedTableMap()
		oldesize = len(self.__table[j])
		self.__table[j][k] = v
		if len(self.__table[j]) > oldsize:
			self.__n += 1

	def __bucket_delitem(self, j, k):
		bucket =  self.__table[j]
		if bucket is None:
			raise KeyError('Key Error: ' + repr(k))
		del bucket[k]

	def __iter__(self):
		for bucket in self.__table:
			if bucket is not None:
				for key in bucket:
					yield key

class ProbeHashMap(HashMapBase):
	'''Hash map implemented with linear probing for collision resolution.'''
	_AVAIL = object() # semtinal marks locations of previous deletions

	def __is_available(self, j):
		'''Return True if index j is available in table.'''
		return self.__table[j] is None or self.__table[j] is ProbeHashMap._AVAIL

	def __find_slot(self, j, k):
		'''Search for key k in bucket at index j.
		Return (seuccess, index) tuple, described ad follows:
		If match was found, success is True and index denotes its location.
		If no match found, success is False and index denotes first avaliable slot.
		'''
		firstAvail = None
		while True:
			if self.__is_available(j):
				if firstAvail is None:
					firstAvail = j
				if self.__table[j] is None:
					return (False, firstAvail)
				elif k == self.__table[j].get_key():
					return (True, j)
				j = (j + 1) % len(self.__table)

	def __bucket_getitem(self, j, k):
		found, s = self.__find_slot(k=j, k)
		if not found:
			raise KeyError('Key Error: ' + repr(k))
		return self.__table[s].get_value()

	def __bucket_setitem(self, j, k, v):
		found, s = self.__find_slot(k=j, k)
		if not found:
			self.__table[s] = self._Item(k, v)
			self.__n += 1
		else:
			self.__table[s].set_value(v)

	def __bucket_delitem(self, j, k):
		found, s = self.__find_slot(k=j, k)
		if not found:
			raise KeyError('Key Error: ' + repr(k))
		self.__table[s] = ProbeHashMap._AVAIL

	def __iter__(self):
		for j in range(len(self,__table)):
			if not self.__is_available(j):
				yield self.__table[j].get_key()

