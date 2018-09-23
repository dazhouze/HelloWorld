#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1132_AVLTreeMap import LinkedBinaryTree

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

		def key(self):
			return self.__key

		def value(self):
			return self.__value

		def set_key(self, k):
			self.__key = k

		def set_value(self, v):
			self.__value = v

class TreeMap(LinkedBinaryTree, MapBase):
	'''Sorted map implementation useing a binary search tree.'''
	class Position(LinkedBinaryTree.Position):
		def key(self):
			'''Return key of map's key-value pair.'''
			return self.element().key()

		def value(self):
			'''Return value of map's key-value pair.'''
			return self.element().value()

	def __subtree_search(self, p, k):
		'''Return Position of p's subtree having key k, or last node searched.'''
		if k == p.key():
			return p
		elif k < p.key():
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
			walk = self.right(wakl)
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
		self.__validate(p)
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
		self.__validate(p)
		if self.right(p):
			return self.__subtree_last_position(self.right(p))
		else:
			walk = p
			above = self.parent(walk)
			while above is not None and walk == self.right(above):
				walk = above
				above  = self.parent(walk)
			return above

	def find_positon(self, k):
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
			return (p.key(), p.value())

	def find_ge(self, k):
		'''Return (key, value) pair with least key greater than or equal to k.
		Return None if there does not exit such a key.
		'''
		if self.is_empty():
			return None
		else:
			p = self.find_position(k)
			if p.key() < k:
				p = self.after(p)
			if p is not None:
				return (p.key(), p.value())
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
				if p.key() < start:
					p = self.after(p)
			while p is not None and (stop is None or p.key() < stop):
				yield (p.key(), p.value())
				p = self.after(p)

	def __getitem__(self, k):
		'''Return value associated with key k(raise KeyError if not found).'''
		if self.is_empty():
			raise KeyError('Key Error: ' + repr(k))
		else:
			p = self.__subtree_search(self.root(), k)
			self.__rebalance_access(p)
			if k != p.key():
				raise KeyError('Key Error: ' + repr(k))
			return p.value()

	def __setitem__(self, k, v):
		'''Assign value v to key k, overwriting existing value if present.'''
		if self.is_empty():
			leaf = self.add_root(self._ITem(k, v))
		else:
			p = self.__subtree_search(self.root(), k)
			if p.key() == k:
				p.element().set_value(v)
				self.__rebalance_access(p)
				return
			else:
				item = self._Item(k, v)
				if p.key() < k:
					leaf = self.add_right(p, item)
				else:
					leaf = self.add_left(p, item)
			self.__rebalance_insert(leaf)

	def __iter__(self):
		'''Generate an iteration of all keys in the map in order.'''
		p = self.first()
		while p is not None:
			yield p.key()
			p = self.after(p)

	def delete(self, p):
		'''Remove the item at given Position.'''
		self.__validate(p)
		if self.left(p) and self.right(p):
			replacement = self.__subtree_last_position(self.left(p))
			self.__replace(p, replacement.element())
			p = replacement
		parent = self.parent(p)
		self.__delete(p)
		self.__rebalance_delete(parent)

	def __delitem__(self, k):
		'''Remove item associated with key k(raise KeyError If not found).'''
		if not self.is_empty():
			p = self.__subtree_search(self.root(), k)
			if k == p.key():
				self.delete(p)
				return
			self.__rebalance_access(p)
		raise KeyError('Key Error: ' + repr(k))

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
		x = p.node()
		y = x.parent()
		z = y.parent()
		if z is None:
			self.__root = x
			x.set_parent(None)
		else:
			self.__relink(z, x, y == z.__left)
		if x == y.left():
			self.__relink(y, x.right(), True)
			self.__relink(x, y, False)
		else:
			self.__relink(y, x.left(), False)
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

class AVLTreeMap(TreeMap):
	'''Sorted map implementation using an AVL tree.'''
	class _Node(TreeMap._Node):
		'''Node class for AVL maintains height value for balanceing.'''
		__slots__ = '__height'
		
		def __init__(self, element, parent=None, left=None, right=None):
			super().__init__(element, parent, left, right)
			self.__height = 0

		def left_height(self):
			if self.__left is not None:
				return self.__left.__height
			return 0

		def right_height(self):
			if self.__right is not None:
				return self.__right.__height
			return 0

		def height(self):
			return self.__height
	
		def set_height(self, h):
			self.__height = h
	
	def  __reconpute_height(self, p):
		node = self.__validate(p)
		node.set_height(1+ max(node.left_height(), node.right_height()))

	def __isbalanced(self, p):
		node = self.__validate(p)
		return abs(node.left_height() - node.right_height()) <= 1

	def __tall_child(self, p, favorleft=False):
		node = self.__validate(p)
		if node.left_height() + (1 if favorleft else 0) > node.right_height():
			return self.left(p)
		else:
			return self.right(p)

	def __tall_grandchild(self, p):
		child = self.__tall_child(p)
		# if child is on left, favor left grandchild:
		#else favor right grandchild 
		alignment = (child == self.left(p))
		return self.__tall_child(child, alignment)

	def __rebalance(self, p):
		while p is not None:
			node = self.__validate(p)
			old_height = node.height()
			if not self.__isbalanced(p):
				p = self.__restructure(self.__tall_grandchild(p)) 
				self.__recompute_height(self.left(p))
				self.__recompute_height(self.right(p))
			self.__reconpute_height(p)
			if node.height() == old_height:
				p = None
			else:
				p = self.parent(p)

	def __rebalance_insert(self, p):
		self.__rebalance(p)

	def __rebalance_delete(self, p):
		self.__rebalance(p)

if __name__ == '__main__':
	alv = AVLTreeMap()
	p = alv.add_root(0)
	print(alv.root())
	for x in range(1, 10+1):
		p = alv.add_right(p, x)
	print(alv.depth(None))
	print(alv.first())
	p = alv.find_positon(5)
	print(p)
