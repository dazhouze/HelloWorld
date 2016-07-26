#!/usr/bin/env python3

#list is array
classMates = []
char = ['a', '33', 'c c']
print classMates
print char
print len (char)
print char[2]
PI = 3.1415926

print '\nPI:%03.2f'% PI
print '\n%2d %02d'% (2,3)
print '\na:%2.5f'% 2.12345
s1 = 10
s2 = 85
r = ((s2 - s1)/s1)
print '\n%2.5f'% ((s2 - s1)/s1)
print '\n%2.5f'% r

print '\nlist initialization'
classMates = ['a', '33b', 'c c']
print classMates[0]
print classMates[1]
print classMates[2]
print classMates[-1]
print classMates[-2]
print classMates[-3]

print '\nadd item to end of list .append'
classMates.append('David')
print classMates

print '\ninsert item to spcific pos of list .insert'
classMates.insert(1, '32b')
print classMates

print '\nget and delet item from the end of list .pop can also design pos in paramter (pos)'
print classMates
print classMates.pop()
print classMates

print '\nchange item to spcific pos by ='
classMates[1] = 'Allen'
print classMates

print '\ntuple is a unchangeble list once initialized. But notice one item tuple should be (1,) with comma'
classTuple = ('12a', '13b', '14c')
print classTuple

