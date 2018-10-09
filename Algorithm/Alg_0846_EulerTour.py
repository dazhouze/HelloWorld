#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0832_LinkedBinaryTree import LinkedBinaryTree
	
def BinaryEulerTour(self):
	'''
	Abstrct base class for performing Euler tour of a tree.
	__hook_previsit and __hook_postvisit may be voerrided by subclasses.
	'''
	def __init__(self, tree):
		'''Prepare a Euler tour template for given tree.'''
		self._tree = tree

	def tree(self):
		'''Return reference to the tree being traversed.'''
		return self._tree

	def excute(self):
		'''Perform the tour and return any result from post visit fo root.'''
		if len(self._tree) > 0:
			return self._tour(self._tree.root(), 0, [])

	def _tour(self, p, d, path):
		'''
		Perform tour of subtree rooted at Position p.
		p	Position of current node being visited
		d	depth of p in the tree
		path list of indices of children on path from root to p
		'''
		results = [None, None]
		self.__hook_previsit(p, d, path)
		if self._tree.left(p) is not None:
			path.append(0)
			results[0] = self._tour(self._tree.left(p), d+1, path)
			path.pop()
		self.__hook_invisit(p, d, path)
		if self._tree.right(p) is not None:
			path.append(1)
			result[1] = self._tour(self._tree.right(p), d+1, path)
			path.pop()
		answer = self.__hook_postvisit(p, d, path, results)
		return answer

	def __hook_previsit(self, p, d, path):
		pass

	def __hook_postvisit(self, p, d, path):
		pass

if __name__ == '__main__':
	lbt = LinkedBinaryTree()
	lbt.test()
