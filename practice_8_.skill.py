print  'Slice'
L = [1, 2, 3, 4, 5, 6]
print L[0:2]
x = 'AB'
for n in range(10):
    print x

print ([x + y + z for x in 'ABC' for y in 'DEF' for z in 'HIG'])
import os
print [d for d in os.listdir('.')]

d = {'x':'A', 'y':'B', 'z':'C'}
for k, v in d.items():
    print 'key: ',k, ' = value: ',v

L = ['Apple', 'B', 'CC', 123]
print [i.lower() for i in L if isinstance(i, str) ]

print 'generator'
L = (x for x in range(1, 11))
print next (L)

def fib (end):
    n, a, b = 0, 0, 1
    while n < end:
        yield b #generator like append item in list
        a, b = b, a+b
        n = n + 1
    #return 'done'

f = fib(1)
for n in f:
    print n
f = fib(-1)
for n in f:
    print n


L = [1, 2, 3]
print L[0]
print 'YHtri:'
def YHtri(line):
    n, a = 0, [1]
    yield a
    while n < line:#n is line num
        n = n+1
        temp = []
        temp.append(1) #add 1 to the begin pos
        i = 0 #i is cloumn num
        while i < n-1:
            i = i + 1
            v= (a[i] + a[i-1])
            temp.append(v)
        temp.append(1) #add 1 to the end pos
        a = temp
        yield a

for n in YHtri(10):
    print n

print 'Iterable'
from collections import Iterable
print isinstance([], Iterable)

