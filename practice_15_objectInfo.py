class Animal (object):
    def run (self):
        print ('Animal is running.')

class Dog (Animal):
    def run (self):
        print ('Dog is running.')

class Cat (Animal):
    def run (self):
        print ('Cat is running.')

a = list()
b = Animal()
c = Dog()

class Tortise (Animal):
    def run(self):
        print ('Tortise is running slowly.')
print (type(123))
print (type('123'))
print (type(a))
print (type(b))
print (type(c))

def fn():
    pass
print (type(fn))
print (type(lambda x:x))
import types
print (type((x for x in range(10)))==types.GeneratorType)

class Husky (Dog):
    def run (self):
        print ('Husky is running')

a = Animal()
b = Dog()
c = Husky()
print( isinstance(c, Husky))
print (dir(c))
