print ('Varibles like __XXX__ are specially used to make difference.')
print ('Exert a enormous function on web programming.')

class Student (object):
    def __init__ (self, name):
        self._name = name
    def __str__ (self):
        return 'Student object (name:%s)'  % self._name
    __repr__ = __str__

print (Student('Bart'))
