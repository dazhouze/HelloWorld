class Student (object):
    pass
s = Student()
s.name = 'BART'
print ('s.name: ', s.name)

def set_age (self, age):
    self.age = age

print ('Bound method(function) to instance')
from types import MethodType
s.setAge = MethodType(set_age, s)
s.setAge(10)
print ('s.age: ', s.age)

s2 = Student()
print ('Bound method(function) to class')

def set_score (self, sc):
    self.score = sc

Student.set_score = set_score
s.set_score(59)
print ('s.score: ', s.score)
s2.set_score(60)
print ('s2.score: ', s2.score)

#class DUT (Student): __slots__ limitation dose not work
class DUT (object):
    __slots__ = ('name', 'age')
d1 = DUT()
d1.name = 'ZZ'
print ('d1.name: ', d1.name)
d1.age = 24
print ('d1.age: ', d1.age)
#d1.score = 100
#print ('d1.score: ', d1.score)


class G114 (object):
    __slots__ = ('score')
g1 = G114()
g1.score = 100
print ('g1.score: ', g1.score)
