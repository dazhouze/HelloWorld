#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
The efficiency of splay trees is due to a certain move-to-root operation, called splaying.
'''

from Alg_1114_TreeMap import TreeMap

class SplayTreeMap(TreeMap):
	'''Sorted map implementation using a splay tree.'''
	def _splay(self, p):
		while p != self.root():
			parent = self.parent(p)
			grand = self.parent(parent)
			if grand is None: # zig case
				self._rotate(p)
			elif (parent == self.left(grand)) == (p == self.left(parent)): # zig-zig
				self._rotate(parent)
				self._rotate(p)
			else: # zig-zag
				self._rotate(p)
				self._rotate(p)

	def _rebalance_insert(self, p):
		self._splay(p)

	def _rebalance_delete(self, p):
		if p is not None:
			self._splay(p)

	def _rebalance_access(self, p):
		self._splay(p)

if __name__ == '__main__':
	stm = SplayTreeMap()
	#print(dir(stm))
	for k in range(65, 65+30):
		v = chr(k)
		stm.setdefault(k, v)
		print('root', (stm.root().key(), stm.root().value()))  # root change
