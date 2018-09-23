class Animal (object):
    pass
class Mammal (Animal):
    pass
class Bird (Animal):
    pass


class RunableMixIn (object):
    def run (self):
        print ('Running ...')

class FlyableMixIn (object):
    def fly (self):
        print ('Flying ...')


class Dog (Mammal, RunableMixIn):
    pass
class Bat (Mammal, RunableMixIn):
    pass

class Parrot (Bird, FlyableMixIn):
    pass
class Ostrich (Bird, FlyableMixIn):
    pass

Hasty = Dog()
print ( isinstance(Hasty, RunableMixIn))
