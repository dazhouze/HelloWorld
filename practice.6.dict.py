d1 = {'m1':-1, 'm2':1, 'm3': 2}
print d1
print (d1['m1'])
key1 = 'm2'
print (d1[key1])

print ('set is only key and no repeat')
s = set([11, 22, '11maseraw'])
print s
print ('set can add item through .add method')
s.add(44)
s.add('biub')
print s
print ('set can remove item through remove')
s.remove(22)
print s


s1 = set([11, 22, 44])
s2 = set([11, 22, 66])
print s1 & s2
print s1 | s2

d2 = {1:1, 2:2, 3:33}
print d2[3]
s2 = set([1, 2, 3])
print s2
s3 = set([1, [2, 3]])
print s3
