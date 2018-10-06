#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import MutableMapping
class MapBase(MutableMapping):
	'''Our own abstract base class that includes a nonpupblic _Item class.'''
	class _Item(object):
		'''Lightweight composite to store key-value pairs as map items.'''
		__slots__ = '_key', '_value'

		def __init__(self, k, v):
			self._key = k
			self._value = v

		def __eq__(self, other):
			return self._key == other._key

		def __ne__(self, other):
			return not (self==other)

		def __It__(self, other):
			return self._key < other._key

		def get_key(self):
			return self._key

		def get_value(self):
			return self._value

		def set_key(self, k):
			self._key = k

		def set_value(self, v):
			self._value = v

