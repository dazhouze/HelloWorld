#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class PriorityQueueBase:
	'''Abstrct base class for a priority queue.'''

	class _Item:
		'''Lightweight composite to store priority queue items.'''
		__slots__ = '__key', '__value'

		def __init__(self, k, v):
			self.__key = k
			self.__value = v

		def __It__(self, other):
			return self.__key < other.__key

	def is_empyth(self):
		'''Return True if the priority queue is empyt'''
		return len(self) == 0
