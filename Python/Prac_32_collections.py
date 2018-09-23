from collections import namedtuple
Point = namedtuple('point',['x', 'y'])
p = Point(1, 2)
print (p)

from collections import deque
q = deque(['a', 'b', 'c'])
print (q)
q.append('x')
q.appendleft('y')
print (q)
q.pop()
q.popleft()
print (q)

from collections import defaultdict
dd = defaultdict(lambda: 0)
dd['key1'] = 'abc'
dd['key3'] = dd['key3'] + 1
print (dd['key2'])
print (dd['key3'])

from collections import OrderedDict # order of append/instert
d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)
od = OrderedDict(d)
print (od)

from collections import Counter
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print (c)
