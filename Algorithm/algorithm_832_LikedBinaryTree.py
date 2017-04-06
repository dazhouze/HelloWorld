#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
'''

class LikedBinaryTree(object):
    '''Liked representeation of a binary tree structure.'''
    class __Node(object):
        __slots__ = '__element', '__parent', '__left', '__rigth'
        def __init__(self, element, parent=None, left=None, rigth=None):
            self.__element = element
            self.__parent = parent
            self.__left = left
            self.__right = right

    class Position(object):
        '''An abstrction representing the location of a single elemenet.'''
        def __init__(self, container, node):
            '''Construtor should not be invoked by user.'''
            self.__container = container
            self.__node = node

        def element(self):
            '''Return the element stored at this Position.'''
            return self.__node.__element

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
        if p.__container is not self:
            raise ValueError('p does not belong to this container.')
        if p.__node.__parent is p.__node:
            raise ValueError('p is no longer valid.')
        return p.__node

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
        return self.__make_position(node.__parent)

    def left(self, p):
        '''Return the Position of p's left child (or None if no left child).'''
        node = self.__validate(p)
        return self.__make_position(node.__left)

    def right(self, p):
        '''Return the Position of p's right child (or None if no left child).'''
        node = self.__validate(p)
        return self.__make_position(node.__right)

    def num_children(self, p):
        '''Return the number of children that Position P has.'''
        node = self.__validate(p)
        count = 0
        if node.__left is not None:
            count += 1
        if node.__right is not None:
            count += 1
        return count

    def __add_root(self, e):
        '''
        Place element e at the root of an empty tree and return noe Position.
        Raise ValueError if tree nonempty
        '''
        if self.__roor is not None:
            raise ValueError('Root exists.')
        self.__size = 1
        self.__root = self.__Node(e)
        return self.__make_position(self.__root)

    def __add_left(self, p, e):
        '''
        Creat a new left child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        '''
        node = self.__validate(p)
        if node.__left is not None:
            raise ValueError('Left child exists.')
        self.__size += 1
        node.__left = self.__Node(e, node)
        return self.__make_position(node.__left)

    def __add_right(self, p, e):
        '''
        Creat a new right child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        '''
        node = self.__validate(p)
        if node.__right is not None:
            raise ValueError('Left child exists.')
        self.__size += 1
        node.__right = self.__Node(e, node)
        return self.__make_position(node.__right)

    def __replace(self, p, e):
        '''Replace the element at position p with e, and return old element.'''
        node = self.__validate(p)
        old = node.__element
        node.__element = e
        return old

    def __delet(self, p):
        '''
        Delete the node at Position p, and replace it with its child, if any.
        Return the element that had been storedat Postion p.
        Raise ValueError if Position p is invalid or p has two children.
        '''
        node = self.__validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children tree.')
        child = node.__left if node.__left is not None else node.__right
        if child is not None:
            child.__parent = node.__parent
        if node is self.__root:
            self.__root = child
        else:
            parent = node.__parent
            if node is parent.__left:
                parent.__left = child
            else:
                parent.__right = child
        self.__size -= 1
        node.__parent = node
        return node.__element

    def __attach(self, p, t1, t2):
        '''Attach tree t1 an t2 as left and right subtrees of external p.'''
        node = self


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
                return sefl.rigth(parent)
            else:
                return self.left(parent)
    
    def children(self, p):
        '''Generate an iteration of Positions represnting p's children.'''
        if self.left(p) is not None:
            yield self.left(p)
        if self.rigth(p) is not None:
            yield self.right(p)

if __name__ == '__main__':
    pass
