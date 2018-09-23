#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0832_LinkedBinaryTree import LinkedBinaryTree
from Alg_1014_MapBase import MapBase

class TreeMap(LinkedBinaryTree, MapBase):
	'''Sorted map implementation useing a binary search tree.'''
	class Position(LinkedBinaryTree.Position):
		def get_key(self):
			'''Return key of map's key-value pair.'''
			return self.get_element().get_key()

		def get_value(self):
			'''Return value of map's key-value pair.'''
			return self.get_element().get_value()

	def __subtree_search(self, p, k):
		'''Return Position of p's subtree having key k, or last node searched.'''
		if k == p.get_key():
			return p
		elif k < p.get_key():
			if self.left(p) is not None:
				return self.__subtree_search(self.left(p), k)
		else:
			if self.right(p) is not None:
				return self.__subtree_search(self.right(p), k)
		return p

	def __subtree_first_position(self, p):
		'''Return Position of first item in subtree rooted at p.'''
		walk = p
		while self.left(walk) is not None:
			walk = self.left(walk)
		return walk

	def __subtree_last_position(self, p):
		'''Return Position of last item in subtree rooted at p.'''
		walk = p
		while self.right(walk) is not None:
			walk = self.right(walk)
		return walk

	def first(self):
		'''Return the first Position in the tree (or None if empty).'''
		if len(self) > 0:
			return self.__subtree_first_position(self.root())
		return None

	def last(self):
		'''Return the last Position in the tree (or None if empty).'''
		if len(self) > 0:
			return self.__subtree_last_position(self.root())
		return None

	def before(self, p):
		'''Return the Position just before p in the natural order.
		Return None if p is the first Postion.
		'''
		self._validate(p)
		if self.left(p):
			return self.__subtree_last_position(self.left(p))
		else:
			walk = p
			above = self.parent(walk)
			while above is not None and walk == self.left(above):
				walk = above
				above  = self.parent(walk)
			return above

	def after(self, p):
		'''Return the Postion just after p in the natural order.
		Return None if p is the last position.
		'''
		self._validate(p)
		if self.right(p):
			return self.__subtree_first_position(self.right(p))
		else:
			walk = p
			above = self.parent(walk)
			while above is not None and walk == self.right(above):
				walk = above
				above  = self.parent(walk)
			return above

	def find_position(self, k):
		'''Return position with key k, or else neighbor (or None if empty).'''
		if self.is_empty():
			return None
		else:
			p  = self.__subtree_search(self.root(), k)
			self.__rebalance_access(p)
			return p

	def find_min(self):
		'''Return (key, value) pair with minimum key (or None if empty).'''
		if self.is_empty():
			return None
		else:
			p = self.first()
			return (p.get_key(), p.get_value())

	def find_max(self):
		'''Return (key,value) pair with maximum key (or None if empty).'''
		if self.is_empty():
			return None
		else:
			p = self.last()
			return (p.get_key(), p.get_value())

	def find_le(self, k):
		'''Return (key, value) pair with greatest key less than or equal to k.
		Return None if there does not exit such a key.
		'''
		if self.is_empty():
			return None
		else:
			p = self.find_position(k)
			if p.get_key() < k:
				p = self.before(p)
			if p is not None:
				return (p.get_key(), p.get_value())
			else:
				return None

	def find_ge(self, k):
		'''Return (key, value) pair with least key greater than or equal to k.
		Return None if there does not exit such a key.
		'''
		if self.is_empty():
			return None
		else:
			p = self.find_position(k)
			if p.get_key() < k:
				p = self.after(p)
			if p is not None:
				return (p.get_key(), p.get_value())
			else:
				return None

	def find_range(self, start, stop):
		'''Iterate all (key, value) pairs such that start <= key < stop.
		If start is None, iteration begins with minimum key of map.
		If stop is None, iteration continuse throught the maximum key of map.
		'''
		if not self.is_empty():
			if start is None:
				p = self.first()
			else:
				p = self.find_position(start)
				if p.get_key() < start:
					p = self.after(p)
			while p is not None and (stop is None or p.get_key() < stop):
				yield (p.get_key(), p.get_value())
				p = self.after(p)

	def __getitem__(self, k):
		'''Return value associated with key k(raise KeyError if not found).'''
		if self.is_empty():
			raise KeyError('Key Error: ' + repr(k))
		else:
			p = self.__subtree_search(self.root(), k)
			self.__rebalance_access(p)
			if k != p.get_key():
				raise KeyError('Key Error: ' + repr(k))
			return p.get_value()

	def __setitem__(self, k, v):
		'''Assign value v to key k, overwriting existing value if present.'''
		if self.is_empty():
			leaf = self.add_root(self._Item(k, v))
		else:
			p = self.__subtree_search(self.root(), k)
			if p.get_key() == k:
				p.get_element().set_get_value(v)
				self.__rebalance_access(p)
				return
			else:
				item = self._Item(k, v)
				if p.get_key() < k:
					leaf = self.add_right(p, item)
				else:
					leaf = self.add_left(p, item)
			self.__rebalance_insert(leaf)

	def __iter__(self):
		'''Generate an iteration of all keys in the map in order.'''
		p = self.first()
		while p is not None:
			yield p.get_key()
			p = self.after(p)

	def delete(self, p):
		'''Remove the item at given Position.'''
		self._validate(p)
		if self.left(p) and self.right(p):
			replacement = self.__subtree_last_position(self.left(p))
			self.__replace(p, replacement.get_element())
			p = replacement
		parent = self.parent(p)
		self.__delete(p)
		self.__rebalance_delete(parent)

	def __delitem__(self, k):
		'''Remove item associated with key k(raise KeyError If not found).'''
		if not self.is_empty():
			p = self.__subtree_search(self.root(), k)
			if k == p.get_key():
				self.delete(p)
				return
			self.__rebalance_access(p)
		raise KeyError('Key Error: ' + repr(k))

	# hooks used by subclasses to balance a tree
	def __rebalance_insert(self, p):
		'''Call to indicate that position p is newly added.'''
		pass
	def __rebalance_delete(self, p):
		'''Call to indicate that a child of p has been removed.'''
		pass
	def __rebalance_access(self, p):
		'''Call to indicate that position p was recently accessed.'''
		pass

	def __relink(self, parent, child, make_left_child):
		'''Relink parent node with chile node (we allow child to be None).'''
		if make_left_child:
			parent.set_left(child)
		else:
			parent.set_right(child)
		if child is not None:
			child.set_parent(parent)

	def __rotate(self, p):
		'''Rotate Position p above its parent.'''
		x = p.get_node()
		y = x.get_parent()
		z = y.get_parent()
		if z is None:
			self.__root = x
			x.set_parent(None)
		else:
			self.__relink(z, x, y == z.__left)
		if x == y.get_left():
			self.__relink(y, x.get_right(), True)
			self.__relink(x, y, False)
		else:
			self.__relink(y, x.get_left(), False)
			self.__relink(x, y, True)

	def __restructure(self, x):
		'''Perform trinode restructure of Position x with parent/grandparent.'''
		y = self.parent(x)
		z = self.parent(y)
		if (x == self.right(y)) == (y == self.right(z)):
			self.__rotate(y)
			return y
		else:
			self.__rotate(x)
			self.__rotate(x)
			return x

if __name__ == '__main__':
	tm = TreeMap()
	for x in range(1, 11):
		tm[x] =  '%d' % x  # map
	print('depth', tm.depth())
	print(tm.first() == tm.root())
	print(tm.last().get_element().get_key())
	print('min',tm.find_min())
	print('max',tm.find_max())
	print('le',tm.find_le(6))
	print('ge',tm.find_ge(3))
	for x in tm.find_range(3,7):
		print(x)
	print(dir(tm))
