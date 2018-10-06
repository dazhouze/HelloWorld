#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedBinaryTree(object):
	'''Linked representeation of a binary tree structure.'''
	class _Node(object):
		__slots__ = '_element', '_parent', '_left', '_right'

		def __init__(self, element, parent=None, left=None, right=None):
			self._element = element
			self._parent = parent
			self._left = left
			self._right = right

		def get_element(self):
			return self._element

		def get_parent(self):
			return self._parent

		def get_left(self):
			return self._left

		def get_right(self):
			return self._right

		def set_element(self, element):
			self._element = element

		def set_parent(self, parent):
			self._parent = parent

		def set_left(self, left):
			self._left = left

		def set_right(self, right):
			self._right = right

	class Position(object):
		'''An abstrction representing the location of a single elemenet.'''
		def __init__(self, container, node):
			'''Construtor should not be invoked by user.'''
			self._container = container  # container is the tree itself. to avoid other tree's position instance
			self._node = node

		def get_container(self):
			'''Return the container of Position.'''
			return self._container

		def get_node(self):
			return self._node

		def __eq__(self, other):
			'''Return True if other Position represents the same location.'''
			return type(other) is type(self) and other._node is self._node

		def __ne__(self, other):
			'''Return True if other dose not represent the same location.'''
			return not(self == other)

	def _validate(self, p):
		'''Return associated node, if position is valid.'''
		if not isinstance(p, self.Position):
			raise TypeError('p must be proper Position type.')
		if p.get_container() is not self:
			raise ValueError('p does not belong to this container.')
		if p.get_node().get_parent() is p.get_node():
			raise ValueError('p is no longer valid.')
		return p.get_node()

	def _make_position(self, node):
		'''Return Position instance for given node (or None if no node).'''
		if node is not None:
			return self.Position(self, node)
		else:
			return None

	def __init__(self):
		'''Create an initially empty binary tree.'''
		self._root = None
		self._size = 0

	def root(self):
		'''Return Position resenting the tree's root(or None if empty).'''
		return self._make_position(self._root)

	def __len__(self):
		'''Return the total number of elements in the tree.'''
		return self._size

	def parent(self, p):
		'''Returen Position representing p's parent (or None if p is root).'''
		node = self._validate(p)
		return self._make_position(node.get_parent())

	def left(self, p):
		'''Return the Position of p's left child (or None if no left child).'''
		node = self._validate(p)
		return self._make_position(node.get_left())

	def right(self, p):
		'''Return the Position of p's right child (or None if no left child).'''
		node = self._validate(p)
		return self._make_position(node.get_right())

	def num_children(self, p):
		'''Return the number of children that Position P has.'''
		node = self._validate(p)
		count = 0
		if node.get_left() is not None:
			count += 1
		if node.get_right() is not None:
			count += 1
		return count

	def add_root(self, e):
		'''
		Place element e at the root of an empty tree and return noe Position.
		Raise ValueError if tree nonempty
		'''
		if self._root is not None:
			raise ValueError('Root exists.')
		self._size = 1
		self._root = self._Node(e)
		return self._make_position(self._root)

	def add_left(self, p, e):
		'''
		Creat a new left child for Position p, storing element e.
		Return the Position of new node.
		Raise ValueError if Position p is invalid or p already has a left child.
		'''
		node = self._validate(p)
		if node.get_left() is not None:
			raise ValueError('Left child exists.')
		self._size += 1
		node.set_left(self._Node(e, node))
		return self._make_position(node.get_left())

	def add_right(self, p, e):
		'''
		Creat a new right child for Position p, storing element e.
		Return the Position of new node.
		Raise ValueError if Position p is invalid or p already has a right child.
		'''
		node = self._validate(p)
		if node.get_right() is not None:
			raise ValueError('Right child exists.')
		self._size += 1
		node.set_right(self._Node(e, node))
		return self._make_position(node.get_right())

	def replace(self, p, e):
		'''Replace the element at position p with e, and return old element.'''
		node = self._validate(p)
		old = node.get_element()
		node.set_element(e)
		return old

	def delete(self, p):
		'''
		Delete the node at Position p, and replace it with its child, if any.
		Return the element that had been storedat Postion p.
		Raise ValueError if Position p is invalid or p has two children.
		'''
		node = self._validate(p)
		if self.num_children(p) == 2:
			raise ValueError('p has two children tree.')
		child = node.get_left() if node.get_left() is not None else node.get_right()
		if child is not None:
			child.set_parent(node.parent)
		if node is self._root:
			self._root = child
		else:
			parent = node.get_parent()
			if node is parent.get_left():
				parent.set_left(child)
			else:
				parent.set_right(child)
		self._size -= 1
		node.set_parent(node)
		return node.get_element()

	def _attach(self, p, t1, t2):
		'''Attach tree t1 an t2 as left and right subtrees of external p.'''
		node = self._validate(p)
		if not self.is_leaf(p):
			raise ValueError('position must be leaf.')
		if not type(self) is type(t1) is type(t2):
			raise TypeError('Tree types must match.')
		self._size += len(t1) + len(t2)
		if not t1.is_empty():
			t1._root.set_parent(node)
			node.set_left(t1._root)
			t1._root = None
			t1._size = 0
		if not t2.is_empty():
			t2._root.set_parent(node)
			node.set_right(t2._root)
			t2._root = None
			t2._size = 0

	def is_root(self, p):
		'''Return True if Position p represents the root of the tree.'''
		return self.root() == p

	def is_leaf(self, p):
		'''Return True if Position p does not have any children.'''
		return self.num_children(p) == 0

	def is_empty(self):
		'''Return True if the tree is empty.'''
		return len(self) == 0

	def depth(self, p=None):
		'''Return the number of levels separation Position p from the root.'''
		if p is None:
			p = self.root()
		if self.is_leaf(p):
			return 0
		return 1 + max(self.height(c) for c in self.children(p))

	def sibling(self, p):
		'''Retrun a Position representing p's sibling (or None if no sibling).'''
		parent = self.parent(p)
		if parent is None:
			return None
		else:
			if p == self.left(parent):
				return self.right(parent)
			else:
				return self.left(parent)

	def children(self, p):
		'''Generate an iteration of Positions represnting p's children.'''
		if self.left(p) is not None:
			yield self.left(p)
		if self.right(p) is not None:
			yield self.right(p)

	def height(self, p=None):
		'''
		Return the height of the subtree rooted at Position p.
		If p is None return the height of entire tree.
		'''
		if p is None:
			p = self.root()
		return self._height2(p)

	def _height2(self, p):
		if self.is_leaf(p):
			return 0
		else:
			return 1 + max(self._height2(c) for c in self.children(p))

if __name__ == '__main__':
	lbt = LinkedBinaryTree()
	pt = lbt.add_root('/')
	print(lbt.parent(pt))
	pl = lbt.add_left(pt, 'Document')
	pr = lbt.add_right(pt, 'Download')
	pr = lbt.delete(pr)
	pr = lbt.add_right(pt, 'Download')
	print(lbt.left(pt).get_node().get_element())
	print(lbt.depth())
	print(lbt.height(pt) , lbt.height(pr), lbt.height(pl))
	print(lbt.children(pt))
	print('parent',lbt.parent(pl).get_node().get_element())
	print(lbt.left(pt).get_node().get_element(), lbt.sibling(pr).get_node().get_element())

	lbt = LinkedBinaryTree()
	p = lbt.add_root(0)
	for x in range(1, 10+1):
		p = lbt.add_right(p, x)
	print(lbt.depth())
	#print(help(lbt))
