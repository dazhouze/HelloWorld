f = abs
print f(-10)
print 'function name is varible'

print 'Higher-order function has function as paramter'
#r = map(x**2, [x for x in range(1, 11)])
'''first paramter has to be function name
note cross lines test'''
r = map(f, [x for x in range(-11, -1)])
print r

print 'reduce function implement all items in Iterable to one'
def add (x, y):
    return 10*x + y
print reduce(add, [x for x in range(10)])


def normalize (x):
    x0 = x[0].upper()
    x1 = x[1:].lower()
    return x0 + x1
L1 = ['adam', 'LISA', 'barT']
L2 = map(normalize, L1)
print(L2)

print 'filter function judge True or False'

def is_palindrome(n):
    L = str(n)
    s = len(L)
    i = 0
    while i < s :
        if not (L[i] is L[s-i-1]):
            return False
        i = i + 1
    if i == 1:
        return False
    return True

print filter(is_palindrome, range(1, 1000))

print sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
'''sort by name in tuple'''
def by_name (i):
    return str.lower(i[0])

def by_num (i):
    return i[1]
print sorted(L, key = by_name)
print sorted(L, key = by_num)

print 'return a function'
print 'function closures should have no loop inside'

print 'lambda is function with no-name'
f = lambda x: x**3
print f(3)

print 'Decorator is a higher order function, paramter is fun, return is fun'


