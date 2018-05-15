print ('Sub-class inherit all method from super-class.')
print ('Sub-class method will over-write the same method in super-class.')

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

print (isinstance(b, Animal))
print (isinstance(c, Animal))
print (isinstance(c, Dog))

def run_twice (animal):
    animal.run()
    animal.run()

run_twice(Animal())
run_twice(Dog())
run_twice(Cat())

class Tortise (Animal):
    def run(self):
        print ('Tortise is running slowly.')

run_twice(Tortise())
