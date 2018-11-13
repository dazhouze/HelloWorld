#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Position class: 
	__init__(): 
		_container: a ref to a instance of the Positional list   _	  _	  _	  _ 
															   <-|_|-><-|_|-><-|_|-><-|_|->   
		_node: a ref to a intance of _Node class	_	
												   <-|_|->  
	__eq__() __ne__()					  
	element()
	_make_position()
	_validate()

_Node class: is the base unit.   
	   _
	<-|_|->
		 __init__()

PositionalList class: positional deque.
	   _	  _	  _	  _ 
	<-|_|-><-|_|-><-|_|-><-|_|->
	basic func:
		__init__()
		__len__()
		__iter__()
		is_empty()
		first()	last()
		before(p)  after(p)
	insert + delete func:
		_insert_between()   __delete_between()
		add_first()		  add_last()
		add_before()		 add_after()
		delet_()
		replace()
'''

class PositionalList(object):
	'''A sequential container of elements allowing positional access.'''
	##### Position class#####
	class Position(object):
		'''An abstraction representing the location of a single element.'''
		def __init__(self, container, node):
			'''Constructor should not be invoked by user.'''
			self._container = container # instance of PositionList class
			self._node = node # instance of _Node class
			
		def element(self):
			'''Return the element stored at this Position.'''
			return self._node._element

		def __eq__(self, other):
			'''Return True if other is a Position represeting the same location.'''
			return type(other) is type(self) and other._node is self._node

		def __ne__(self, other):
			'''Retrun True if other does not represent the same loaction.'''
			return not (self == other)

	##### utility method #####
	def _validate(self, p):
		'''Return position's node, or raise approprate error if invalid.'''
		if not isinstance(p, self.Position):
			raise TypeError('p must be proper Position type')
		if p._container is not self:
			raise ValueError('p does not belong to this container')
		if p._node._next is None:
			raise ValueError('p is no longer valid')
		return p._node

	def _make_position(self, node):
		'''Return Position instance for given node (or None if sentinel).'''
		if node is self._header or node is self._trailer:
			return None
		return self.Position(self, node)

	##### _Node class #####
	class _Node(object):
		'''Lightweigth, nonpublic class for storing a double linked node.'''
		__slots__ = '_element', '_prev', '_next'

		def __init__(self, e, p, n):
			self._element = e
			self._prev = p
			self._next = n

	##### Positional list class #####
	def __init__(self):
		'''Creat an empty list'''
		self._header = self._Node(None, None, None)
		self._trailer = self._Node(None, None, None)
		self._header._next = self._trailer
		self._trailer._prev = self._header
		self._size = 0

	def __len__(self):
		'''Return the number of elements in the list.'''
		return self._size

	def is_empty(self):
		'''Return True if the list is empty.'''
		return self._size == 0

	##### accessors #####
	def first(self):
		'''Return the first Position in the list (or None if list is empty).'''
		return self._make_position(self._header._next)

	def last(self):
		'''Return the first Position in the list (or None if list is empty).'''
		return self._make_position(self._trailer._prev)

	def before(self, p):
		'''Return the Position just before Position p (or None if p is first).'''
		node = self._validate(p)
		return self._make_position(node._prev)
	
	def after(self, p):
		'''Return the Position just after Position p (or None if p is last).'''
		node = self._validate(p)
		return self._make_position(node._next)

	def __iter__(self):
		'''Generatea forward iteration of the elements of the list.'''
		cursor = self.first()
		while cursor is not None:
			yield cursor._node._element
			cursor = self.after(cursor)

	##### mutators #####
	def _insert_between(self, e, predecessor, successor):
		'''Add element e between two existing nodes and return new node.'''
		newest = self._Node(e, predecessor, successor)
		predecessor._next = newest
		successor._prev = newest
		self._size += 1
		return self._make_position(newest)

	def _delete_node(self, node):
		'''Delete nonsentinel node from the list and returen its element.'''
		predecessor = node._prev
		successor = node._next
		predecessor._next = successor
		successor._prev = predecessor
		self._size -= 1
		element = node._element
		node._prev = None
		node._next = None
		node._element = None
		return element

	def add_first(self, e):
		'''Insert element e at the font  of the list and return new Postion.'''
		return self._insert_between(e, self._header, self._header._next)

	def add_last(self, e):
		'''Insert element e at the back of the list and return new position.'''
		return self._insert_between(e, self._trailer._prev, self._trailer)
	
	def add_before(self, p, e):
		'''Insert element e into list after Positon p and return new Postion.'''
		original = self._validate(p)
		return self._insert_between(e, original._prev, original)

	def add_after(self, p, e):
		'''Insert element e into list after Position pand return new Position.'''
		original = self._validate(p)
		return self._insert_between(e, original, original._next)

	def delete(self, p):
		'''Remove and return the elemet at Position p.'''
		original = self._validate(p)
		return self._delete_node(original)

	def replace(self, p, e):
		'''
		Replase the element at Position p.
		Retrun the element formerly at Position p.
		'''
		original = self._validate(p)  # _Node object
		old_value = original._element
		original._element = e
		return old_value

if __name__ == '__main__':
	PL = PositionalList()
	p1 = PL.add_first('H')
	p2 = PL.add_after(p1, 'E')
	p5 = PL.add_last('O')
	p4 = PL.add_before(p5, 'L')
	p3 = PL.add_before(p4, 'L')
	p3 = PL.replace(p3, 'l')
	p = PL.last()
	for x in ' WORLD':
		p = PL.add_after(p, x)
	print('length of PositionalList:%d'%len(PL))
	print(PL.first()._node._element)
	for x in PL:
		print(x, end = ' ')
	print('')
