#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinkedBinaryTree(object):
    '''Linked representeation of a binary tree structure.'''
    class _Node(object):
        __slots__ = '__element', '__parent', '__left', '__right'

        def __init__(self, element, parent=None, left=None, right=None):
            self.__element = element
            self.__parent = parent
            self.__left = left
            self.__right = right

        def get_element(self):
            return self.__element

        def get_parent(self):
            return self.__parent

        def get_left(self):
            return self.__left

        def get_right(self):
            return self.__right

        def set_element(self, element):
            self.__element = element

        def set_parent(self, parent):
            self.__parent = parent

        def set_left(self, left):
            self.__left = left

        def set_right(self, right):
            self.__right = right

    class Position(object):
        '''An abstrction representing the location of a single elemenet.'''
        def __init__(self, container, node):
            '''Construtor should not be invoked by user.'''
            self.__container = container  # container is the tree itself. to avoid other tree's position instance
            self.__node = node

        def get_element(self):
            '''Return the element stored at this Position.'''
            return self.__node.get_element()

        def get_container(self):
            '''Return the container of Position.'''
            return self.__container

        def get_node(self):
            return self.__node

        def __eq__(self, other):
            '''Return True if other Position represents the same location.'''
            return type(other) is type(self) and other.__node is self.__node

        def __ne__(self, other):
            '''Return True if other dose not represent the same location.'''
            return not(self == other)

    def __validate(self, p):
        '''Return associated node, if position is valid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type.')
        if p.get_container() is not self:
            raise ValueError('p does not belong to this container.')
        if p.get_node().get_parent() is p.get_node():
            raise ValueError('p is no longer valid.')
        return p.get_node()

    def __make_position(self, node):
        '''Return Position instance for given node (or None if no node).'''
        if node is not None:
            return self.Position(self, node)
        else:
            return None

    def __init__(self):
        '''Create an initially empty binary tree.'''
        self.__root = None
        self.__size = 0

    def root(self):
        '''Return Position resenting the tree's root(or None if empty).'''
        return self.__make_position(self.__root)

    def __len__(self):
        '''Return the total number of elements in the tree.'''
        return self.__size

    def parent(self, p):
        '''Returen Position representing p's parent (or None if p is root).'''
        node = self.__validate(p)
        return self.__make_position(node.get_parent())

    def left(self, p):
        '''Return the Position of p's left child (or None if no left child).'''
        node = self.__validate(p)
        return self.__make_position(node.get_left())

    def right(self, p):
        '''Return the Position of p's right child (or None if no left child).'''
        node = self.__validate(p)
        return self.__make_position(node.get_right())

    def num_children(self, p):
        '''Return the number of children that Position P has.'''
        node = self.__validate(p)
        count = 0
        if node.get_left() is not None:
            count += 1
        if node.get_right() is not None:
            count += 1
        return count

    def __add_root(self, e):
        '''
        Place element e at the root of an empty tree and return noe Position.
        Raise ValueError if tree nonempty
        '''
        if self.__root is not None:
            raise ValueError('Root exists.')
        self.__size = 1
        self.__root = self._Node(e)
        return self.__make_position(self.__root)

    def __add_left(self, p, e):
        '''
        Creat a new left child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        '''
        node = self.__validate(p)
        if node.get_left() is not None:
            raise ValueError('Left child exists.')
        self.__size += 1
        node.set_left(self._Node(e, node))
        return self.__make_position(node.get_left())

    def __add_right(self, p, e):
        '''
        Creat a new right child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        '''
        node = self.__validate(p)
        if node.get_right() is not None:
            raise ValueError('Left child exists.')
        self.__size += 1
        node.set_right(self._Node(e, node))
        return self.__make_position(node.get_right())

    def __replace(self, p, e):
        '''Replace the element at position p with e, and return old element.'''
        node = self.__validate(p)
        old = node.get_element()
        node.set_element(e)
        return old

    def __delete(self, p):
        '''
        Delete the node at Position p, and replace it with its child, if any.
        Return the element that had been storedat Position p.
        Raise ValueError if Position p is invalid or p has two children.
        '''
        node = self.__validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children tree.')
        child = node.get_left() if node.get_left() is not None else node.get_right()
        if child is not None:
            child.set_parent(node.parent)
        if node is self.__root:
            self.__root = child
        else:
            parent = node.get_parent()
            if node is parent.get_left():
                parent.set_left(child)
            else:
                parent.set_right(child)
        self.__size -= 1
        node.set_parent(node)
        return node.get_element()

    def __attach(self, p, t1, t2):
        '''Attach tree t1 an t2 as left and right subtrees of external p.'''
        node = self.__validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf.')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match.')
        self.__size += len(t1) + len(t2)
        if not t1.is_empty():
            t1.__root.set_parent(node)
            node.set_left(t1.__root)
            t1.__root = None
            t1.__size = 0
        if not t2.is_empty():
            t2.__root.set_parent(node)
            node.set_right(t2.__root)
            t2.__root = None
            t2.__size = 0

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
        if p is None:
            p = self.root()
        if self.is_leaf(p):
            return 0
        return 1 + max(self.heigt(c) for c in self.children(p))

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
        if self.is_leaf(p):
            return 0
        return 1 + max(self. height2(c) for c in self.children(p))

class MapBase(object):
    '''Our own abstract base class that includes a nonpupblic _Item class.'''
    class _Item(object):
        '''Lightweight composite to store key-value pairs as map items.'''
        __slots__ = '__key', '__value'

        def __init__(self, k, v);
            self.__key = k
            self.__value = v

        def __eq__(self, other):
            return self.__key == other.__key

        def __ne__(self, other):
            return not (self==other)

        def __It__(self, other):
            return self.__key < other.__key

        def get_key(self):
            return self.__key

        def get_value(self):
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
            return self.element().get_key()

        def value(self):
            '''Return value of map's key-value pair.'''
            return self.element().get_value()

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
            p  = self.__subtree._search(self.root(), k)
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
            leaf = self.__add_root(self._ITem(k, v))
        else:
            p = self.__subtree_search(self.root(), k)
            if p.key() == k:
                p.element().set_value(v)
                self.__rebalance_access(p)
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self.__add_right(p, item)
                else:
                    leaf = self.__add_left(p, item)
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
        if not self.is_empth():
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

    class SplayTreeMap(TreeMap):
        '''Sorted map implementation using a splay tree.'''
        def __splay(self, p):
            while p != self.root():
                parent = self.parent(p)
                grand = self.parent(parent)
                if grand is None: # zig case
                    self.__rotate(p)
                elif (parent == self.left(grand)) == (p == self.left(parent)): # zig-zig
                    self.__rotate(parent)
                    self.__rotate(p)
                else: # zig-zag
                    self.__rotate(p)
                    self.__rotate(p)

        def __rebalance_insert(self, p):
            self.__splay(p)

        def __rebalance_delete(self, p):
            if p is not None:
                self.__splay(p)

        def __rebalance_access(self, p):
            self.__splay(p)
