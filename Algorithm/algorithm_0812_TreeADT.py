#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A Tree Abstract Base Class.
'''
class Tree(object):
	'''Abstract base class representing a tree structure.'''
	class Position(object):
		'''An abstrction representing the location of a single elemenet.'''
		def element(self):
			'''Return the element stored at this Position.'''
			raise NotImplementedError('must be implemented by subclass!')

		def __eq__(self, other):
			'''Return True if other Position represents the same location.'''
			raise NotImplementedError('must be implemented by subclass!')

		def __ne__(self, other):
			'''Return True if other dose not represent the same location.'''
			return not(self == other)

	def root(self):
		'''Return Position resenting the tree's root(or None if empty).'''
		raise NotImplementedError('must be implemented by subclass!')

	def parent(self, p):
		'''Returen Position representing p's parent (or None if p is root).'''
		raise NotImplementedError('must be implemented by subclass!')

	def num_children(self, p):
		'''Return the number of children that Position P has.'''
		raise NotImplementedError('must be implemented by subclass!')

	def children(self, p):
		'''Generate an iteration of Positions representing p's children.'''
		raise NotImplementedError('must be implemented by subclass!')

	def __len__(self):
		'''Return the total number of elements in the tree.'''
		raise NotImplementedError('must be implemented by subclass!')

	def is_root(self, p):
		'''Return True if Position p represents the root of the tree.'''
		return self.root() == p

	def is_leaf(self, p):
		'''Return True if Position p does not have any children.'''
		return self.num_children(p) == 0

	def is_empty(self):
		'''Return True if the tree is empty.'''
		return len(self) == 0

	def depth(self, p):
		'''Return the number of levels separation Position p from the root.'''
		if not is_root(p):
			return self.depth(self.parent(p)) + 1
		return 0

	def height(self, p=None):
		'''Return the heigth of p.
		If p is a leaf, then the height of p is 0.
		Otherwise, the height of p is one more than the maximum of the heights of p’s children.
		If p is None return the height of entire tree.
		'''
		if p is None:
			p = self.root()
		if self.is_leaf(p):
			return 0
		return 1 + max(self.heigt(c) for c in self.children(p))

if __name__ == '__main__':
	pass
