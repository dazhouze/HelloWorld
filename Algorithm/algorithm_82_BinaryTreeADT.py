#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A binary tree is an ordered tree with the following properties:
1. Every node has at most two children.
2. Each child node is labeled as being either a left child or a right child.
3. A left child precedes a right child in the order of children of a node.
'''
class BinaryTree(object):
    '''Abstract base class representing a binary tree structure.'''
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
        '''Return True if Postion p represents the root of the tree.'''
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

    def left(self, p):
        '''
        Return a Position representing p's left child.
        Return None if p does not have a left child.
        '''
        raise NotImplementedError('must be implemented by subclass!')

    def right(self, p):
        '''
        Return a Position representing p's right clild.
        Return None if p does not have a rigth chile.
        '''
        raise NotImplementedError('must be implemented by subclass!')

    def sibling(self, p):
        '''Retrun a Postion representing p's sibling (or None if no sibling).'''
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return sefl.rigth(parent)
            else:
                return self.left(parent)
    
    def children(self, p):
        '''Generate an iteration of Postions represnting p's children.'''
        if self.left(p) is not None:
            yield self.left(p)
        if self.rigth(p) is not None:
            yield self.right(p)

if __name__ == '__main__':
    pass
