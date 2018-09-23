print max (1, 2, 3)
n1 = 100
n2 = 199
print hex(n1)
print hex(n2)

def my_abs (x):
    if x >= 0:
        return x
    else:
        return  -x

print my_abs(1)
print my_abs(-1)

print '\nlib abs:'
#print abs('def')

def my_abs2 (x):
    if not isinstance(x,(int, float)):
        raise TypeError("Bad type.")
    if x >= 0:
        return x
    else:
        return  -x

#print my_abs2('abc')

import math

def move (x, y, step, angle):
    nx = x + step * math.cos(angle)
    ny = y + step * math.sin(angle)
    return nx, ny

x, y = move (100, 100, 10, 45)
print x, y

def quadratic(a, b, c):
    if ((b**2 - 4*a*c) > 0):
        solution1 = (math.sqrt(b**2 - 4*a*c) - b)/2/a
        solution2 = (-math.sqrt(b**2 - 4*a*c) - b)/2/a
        return solution1, solution2
    elif ((b**2 - 4*a*c) == 0):
        return - b/2/a
    else:
        return None, None
x, y = quadratic(-2, 5, 1)
print 'The answer of is'
print x, y

def power (x, n = 2):
    i = 1;
    while (i < n):
        x *= x
        i += 1
    return x
print power(3)
print power(3, 2)

def cal (*num):
    s = 0
    for n in num:
        s += n
    return s
print cal(1, 2, 3, 4)
num = (1, 3, 2, 4, 5)
print cal(*num)

def add (n):
    if (n == 1):
        return '1'
    else:
        return n.join('n', add(n))
print 'recursion',10, add(10)
