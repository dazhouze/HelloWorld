#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
hash function is to map each key to an integer in range[0, N-1], N is capacity of bucket array for a hash table.
hash function: 1. hash code, 2. compression function.

arbitrary objects
	 |hash code
	\|/
hash code (..-2,-1,0,1,2...)
	 |compression function
	\|/
0,1,2...N-1

Two implementations of a hash table,
one using separate chaining 
and the other using open addressing with linear probing. 
'''

from Alg_1014_MapBase import MapBase
from Alg_1015_UnsortedTableMap import UnsortedTableMap
from random import randrange 

class HashMapBase(MapBase):
	'''Abstract base class for map using hash-table with MAD compression.'''
	def __init__(self, cap=11, p=109345121):
		'''Create an empty hash-table map.'''
		self._table = [None for x in range(cap)]
		self._n = 0
		self._prime = p
		self._scale = 1 + randrange(p-1)
		self._shift = randrange(p)

	def _hash_function(self, k):
		return (hash(k)*self._scale + self._shift) % self._prime % len(self._table)

	def __len__(self):
		return self._n

	def __getitem__(self, k):
		j = self._hash_function(k)
		return self._bucket_getitem(j, k)

	def __setitem__(self, k, v):
		j = self._hash_function(k)
		self._bucket_setitem(j, k, v)
		if self._n > len(self._table) // 2:
			self._resize(2*len(self._table) - 1)

	def __delitem__(self, k):
		j = self._hash_function(k)
		self._bucket_delitem(j, k)
		self._n -= 1

	def _resize(self, c):
		old = list(self.items())
		self._table = c * [None]
		self._n = 0
		for (k, v) in old:
			self[k] = v

# separate chaining
class ChainHashMap(HashMapBase):
	'''Hash map implemented with separate chaining for collision resolution.'''
	def _bucket_getitem(self, j, k):
		bucket = self._table[j]
		if bucket is None:
			raise KeyError('Key Error: ' + repr(k))
		return bucket[k]

	def _bucket_setitem(self, j, k, v):
		if self._table[j] is None:
			self._table[j] = UnsortedTableMap()
		oldsize = len(self._table[j])
		self._table[j][k] = v
		if len(self._table[j]) > oldsize:
			self._n += 1

	def _bucket_delitem(self, j, k):
		bucket =  self._table[j]
		if bucket is None:
			raise KeyError('Key Error: ' + repr(k))
		del bucket[k]

	def __iter__(self):
		for bucket in self._table:
			if bucket is not None:
				for key in bucket:
					yield key

# linear probing
class ProbeHashMap(HashMapBase):
	'''Hash map implemented with linear probing for collision resolution.'''
	_AVAIL = object() # semtinal marks locations of previous deletions

	def _is_available(self, j):
		'''Return True if index j is available in table.'''
		return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

	def _find_slot(self, j, k):
		'''Search for key k in bucket at index j.
		Return (seuccess, index) tuple, described ad follows:
		If match was found, success is True and index denotes its location.
		If no match found, success is False and index denotes first avaliable slot.
		'''
		firstAvail = None
		while True:
			if self._is_available(j):
				if firstAvail is None:
					firstAvail = j
				if self._table[j] is None:
					return (False, firstAvail)
			elif k == self._table[j]._key:
				return (True, j)
			j = (j + 1) % len(self._table)

	def _bucket_getitem(self, j, k):
		found, s = self._find_slot(j, k)
		if not found:
			raise KeyError('Key Error: ' + repr(k))
		return self._table[s]._value

	def _bucket_setitem(self, j, k, v):
		found, s = self._find_slot(j, k)
		if not found:
			self._table[s] = self._Item(k, v)
			self._n += 1
		else:
			self._table[s]._value = v

	def _bucket_delitem(self, j, k):
		found, s = self._find_slot(j, k)
		if not found:
			raise KeyError('Key Error: ' + repr(k))
		self._table[s] = ProbeHashMap._AVAIL

	def __iter__(self):
		for j in range(len(self._table)):
			if not self._is_available(j):
				yield self._table[j]._key

if __name__ == '__main__':
	chm =  ChainHashMap()
	for test in (ChainHashMap(), ProbeHashMap()):
		print(type(test))
		for k in range(26):
			v = chr(k+65)
			#print('set', k, v)
			test.setdefault(k, v)
		print(len(test))
		for k,v in sorted(test.items()):
			print('get', k, v)
