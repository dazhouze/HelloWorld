#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Position class: 
    __init__(): 
        __container: a ref to a instance of the Positional list   _      _      _      _ 
                                                               <-|_|-><-|_|-><-|_|-><-|_|->   
        __node: a ref to a intance of __Node class    _    
                                                   <-|_|->  
    __eq__() __ne__()                      
    element()
    __make_position()
    __validate()

__Node class: is the base unit.   
       _
    <-|_|->
         __init__()
         getPrev()    setPrev()
         getNext()    setNext()
         getElement() setElement()

PositionalList class: positional deque.
       _      _      _      _ 
    <-|_|-><-|_|-><-|_|-><-|_|->
    basic func:
        __init__()
        __len__()
        __iter__()
        is_empty()
        first()    last()
        before(p)  after(p)
    insert + delete func:
        __insert_between()   __delete_between()
        add_first()          add_last()
        add_before()         add_after()
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
            self.__container = container # instance of PositionList class
            self.__node = node # instance of __Node class
            
        def getContainer(self):
            return self.__container

        def getNode(self):
            return self.__node

        def element(self):
            '''Return the element stored at this Position.'''
            return self.getNode().getElement()

        def __eq__(self, other):
            '''Return True if other is a Position represeting the same location.'''
            return type(other) is type(self) and other.getNode() is self.getNode()

        def __ne__(self, other):
            '''Retrun True if other does not represent the same loaction.'''
            return not (self == other)

    ##### utility method #####
    def __validate(self, p):
        '''Return position's node, or raise approprate error if invalid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.getContainer() is not self:
            raise ValueError('p does not belong to this container')
        if p.getNode().getNext() is None:
            raise ValueError('p is no longer valid')
        return p.getNode()

    def __make_position(self, node):
        '''Return Position instance for given node (or None if sentinel).'''
        if node is self.__header or node is self.__trailer:
            return None
        return self.Position(self, node)

    ##### __Node class #####
    class __Node(object):
        '''Lightweigth, nonpublic class for storing a double linked node.'''
        __slots__ = '__element', '__prev', '__next'

        def __init__(self, e, p, n):
            self.__element = e
            self.__prev = p
            self.__next = n

        def getPrev(self):
            return self.__prev

        def getNext(self):
            return self.__next

        def getElement(self):
            return self.__element

        def setPrev(self, p):
            self.__prev = p

        def setNext(self, n):
            self.__next = n

        def setElement(self, e):
            self.__element = e

    ##### Positional list class #####
    def __init__(self):
        '''Creat an empty list'''
        self.__header = self.__Node(None, None, None)
        self.__trailer = self.__Node(None, None, None)
        self.__header.setNext(self.__trailer)
        self.__trailer.setPrev(self.__header)
        self.__size = 0

    def __len__(self):
        '''Return the number of elements in the list.'''
        return self.__size

    def is_empty(self):
        '''Return True if the list is empty.'''
        return self.__size == 0


    ##### accessors #####
    def first(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__header.getNext())

    def last(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self.__make_position(self.__trailer.getPrev())

    def before(self, p):
        '''Return the Position just before Position p (or None if p is first).'''
        node = self.__validate(p)
        return self.__make_position(node.getPrev())
    
    def after(self, p):
        '''Return the Position just after Position p (or None if p is last).'''
        node = self.__validate(p)
        return self.__make_position(node.getNext())

    def __iter__(self):
        '''Generatea forward iteration of the elements of the list.'''
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    ##### mutators #####
    def __insert_between(self, e, predecessor, successor):
        '''Add element e between two existing nodes and return new node.'''
        newest = self.__Node(e, predecessor, successor)
        predecessor.setNext(newest)
        successor.setPrev(newest)
        self.__size += 1
        return self.__make_position(newest)

    def __delete_node(self, node):
        '''Delete nonsentinel node from the list and returen its element.'''
        predecessor = node.getPrev()
        successor = node.getNext()
        predecessor.setNext(successor)
        successor.setPrev(predecessor)
        self.__size -= 1
        element = node.getElement()
        node.setPrev(None)
        node.setNext(None)
        node.setElement(None)
        return element

    def add_first(self, e):
        '''Insert element e at the font  of the list and return new Postion.'''
        return self.__insert_between(e, self.__header, self.__header.getNext())

    def add_last(self, e):
        '''Insert element e at the back of the list and return new position.'''
        return self.__insert_between(e, self.__trailer.getPrev(), self.__trailer)
    
    def add_before(self, p, e):
        '''Insert element e into list after Positon p and return new Postion.'''
        original = self.__validate(p)
        return self.__insert_between(e, original.getPrev(), original)

    def add_after(self, p, e):
        '''Insert element e into list after Position pand return new Position.'''
        original = self.__validate(p)
        return self.__insert_between(e, original, original.getNext())

    def delete(self, p):
        '''Remove and return the elemet at Position p.'''
        original = self.__validate(p)
        return self.__delete_node(original)

    def replace(self, p, e):
        '''
        Replase the element at Position p.
        Retrun the element formerly at Position p.
        '''
        original = self.__validate(p)
        old_value = orginal.getElement()
        original.setElement(e)
        return old_value


'''
FavoritesList: based on PositionalList()
    __Item(): value and count
    __init__(): PositionalList()
    __len__:
    is_empty:
    access(): __Item.value
    top():
    remove():
    __find_position(): fine target element in PositionalList
    __move_up():
    
'''
class FavoritesListMTF(object):
    '''List of elementsordered from most frequently accessed to least.'''
    ##### nested __Item class #####
    class __Item(object):
        __slots__ = '__value', '__count'
        def __init__(self,e):
            self.__value = e
            self.__count = 0

        def getValue(self):
            '''Return the value of __Item.'''
            return self.__value

        def getCount(self):
            '''Return the count of __Item.'''
            return self.__count

        def addCount(self):
            '''Add 1 to the count of __Item.'''
            self.__count += 1

    ##### nonpublic utilities of class FavoritesList #####
    def __find_position(self, e):
        '''Search for element e and return its Position (or None if not found).'''
        walk = self.__data.first()
        while walk is not None and walk.element().getValue() != e:
            walk = self.__data.after(walk)
        return walk

    def __move_up(self, p):
        '''Move item at Postion p earlier in the list based on access count.'''
        if p != self.__data.first():
            self.__data.add_first(self.__data.delete(p)) # delete p and re-insert at first

    ##### public utilities of class FavoritesList #####
    def __init__(self):
        '''Create an empty list of favorites.'''
        self.__data = PositionalList() #
    
    def __len__(self):
        '''Return number of entries on favorites list.'''
        return len(self.__data)

    def is_empty(self):
        '''Retrun True if the list is empty.'''
        return len(self.__data)==0

    def access(self, e):
        '''Access element e, thereby increasing its access count.'''
        p = self.__find_position(e) # try to locate existing element
        if p is None:
            p = self.__data.add_last(self.__Item(e))
        p.element().addCount() # count += 1
        self.__move_up(p)

    def remove(self, e):
        '''Remove element e frome the list of favorites.'''
        p = self.__find_position(e)
        if p is not None:
            self.__data.delete(p)

    def top(self, k):
        '''Generate sequence of topk elements in terms of access count.'''
        if not 1<= k <= len(self):
            raise ValueError('Illegal value for k.')
        #begin by makeing a copy of the original list
        temp = PositionalList()
        for item in self.__data:
            temp.add_last(item)
        print('len temp:',len(temp))
        for j in range(0, k):
            highPos = temp.first() # position container
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element().getCount() > highPos.element().getCount():
                    highPos = walk
                walk = temp.after(walk) # next position in PositionalList
            # the element with highest count
            yield highPos.element().getValue()
            temp.delete(highPos)

if __name__ == '__main__':
    FL = FavoritesListMTF()
    FL.access(1)
    FL.access(2)
    FL.access(2)
    FL.access(3)
    FL.access(3)
    FL.access(3)
    top = FL.top(3)
    for x in range(0,2):
        print(x,next(top))
