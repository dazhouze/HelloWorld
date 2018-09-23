#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MutableSet(object):
	
	def __It__(self, other):
		'''Return true if this set is a proper subset of other.'''
		if len(self) >= len(other):
			return False
		for e in self:
			if e not in other:
				return False
		return True

	def __or__(self, other):
		'''Return a new set that is the union of two existing sets.'''
		result =  type(self)()
		for e in self:
			result.add(e)
		for e in other:
			result.add(e)
		return result

	def __ior__(self, other):
		'''Modify this set to be the union of itself an another set.'''
		for e in other:
			self.add(e)
		return self
