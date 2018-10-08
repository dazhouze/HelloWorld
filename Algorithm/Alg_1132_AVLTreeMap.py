#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1114_TreeMap import TreeMap

class AVLTreeMap(TreeMap):
	'''Sorted map implementation using an AVL tree.'''
	class _Node(TreeMap._Node):
		'''Node class for AVL maintains height value for balanceing.'''
		__slots__ = '_height'
		
		def __init__(self, element, parent=None, left=None, right=None):
			super().__init__(element, parent, left, right)
			self._height = 0

		def left_height(self):
			if self.get_left() is not None:
				return self._left._height
			return 0

		def right_height(self):
			if self.get_right() is not None:
				return self._right._height
			return 0

		def get_height(self):
			return self._height
	
		def set_height(self, h):
			self._height = h
	
	def _recompute_height(self, p):
		node = self._validate(p)
		node.set_height(1+ max(node.left_height(), node.right_height()))

	def _isbalanced(self, p):
		node = self._validate(p)
		return abs(node.left_height() - node.right_height()) <= 1

	def _tall_child(self, p, favorleft=False):
		node = self._validate(p)
		if node.left_height() + (1 if favorleft else 0) > node.right_height():
			return self.left(p)
		else:
			return self.right(p)

	def _tall_grandchild(self, p):
		child = self._tall_child(p)
		# if child is on left, favor left grandchild:
		#else favor right grandchild 
		alignment = (child == self.left(p))
		return self._tall_child(child, alignment)

	# override balancing hooks, it is the balancing method for AVL tree
	def _rebalance(self, p):
		while p is not None:
			node = self._validate(p)
			old_height = node.get_height()
			if not self._isbalanced(p):
				p = self._restructure(self._tall_grandchild(p)) 
				self._recompute_height(self.left(p))
				self._recompute_height(self.right(p))
			self._recompute_height(p)
			if node.get_height() == old_height:
				p = None
			else:
				p = self.parent(p)

	def _rebalance_insert(self, p):
		self._rebalance(p)

	def _rebalance_delete(self, p):
		self._rebalance(p)

	def find_close(self, k):
		'''Return (key, value) pair with closest key to k.
		Return None if there does not exit such a key.
		'''
		if self.is_empty():
			return None
		else:
			p = self.find_position(k)
			if p is None:
				return None
			min_dist, min_p = float('Inf'), None
			for pos in (self.before(p), p, self.after(p),):
				if pos is None:
					continue
				dist = abs(pos.key() - k)
				if dist < min_dist:
					min_dist, min_p = dist, pos
			p = min_p
			return (p.key(), p.value())

if __name__ == '__main__':
	avl = AVLTreeMap()
	'''
	for x in range(1, 10):
		print('####',x,)
		avl.setdefault(x, '%d' % (x))  # map
		print('depth', avl.depth(), 'num', len(avl))
		print('left rigth heigth', avl.root().get_node().left_height(), avl.root().get_node().right_height())
	'''
	for x in range(16, 31):
		avl.setdefault(x, '%d' % (x))  # map
	for k,v in sorted(avl.items()):
		print(k, v)
	k = 15
	close_k, close_y = avl.find_close(k)
	print('close',close_k)
	'''
	print(avl.first() == avl.root())
	print(avl.last().get_element().get_key())
	print('min',avl.find_min())
	print('max',avl.find_max())
	print('le',avl.find_le(6))
	'''
