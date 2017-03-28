#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Zhou Ze'
__version__ = '0.0.1'

'''
Tuple based stack class 2 items.
'''

class Stack (object):
    '''matched base stack. Tuple based implementation'''

    def __init__(self, *start):
        self.__stack = None
        for i in range(0, len(start), 2):
            self.push(start[i], start[i+1])

    def push(self, base, qual):
        self.__stack = base, qual, self.__stack

    def pop(self):
        base, qual, self.__stack = self.__stack
        return base, qual

    def is_empty(self):
        if self.__stack:
            return len(self.__stack)==0
        else:
            return True

    def __len__(self):
        len, tree = 0, self.__stack
        while tree:
            len, tree = len+1, tree[2]
        return len

    def __repr__(self):
        return '[FastStack:'+repr(self.__stack)+']'

if __name__ == '__main__':
    x=Stack(-8,'abcd')
    y=Stack()
    z=Stack()
    print(x,x.is_empty())
    print(y,y.is_empty())
    z.push('Insertion',[3, 4, 2])
    for b,q in zip('A','1'):
        x.push(b,q)
    x.push('Insertion',[3, 4, 2])
    for b,q in zip('b','2'):
        x.push(b,q)
    print('x:', x)
    print('y:', y)
    print('z:', z)
    while x:
        print(x.pop())
