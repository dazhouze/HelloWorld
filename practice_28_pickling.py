print ('Pickling processing make varible to be storible.')

import pickle
d = {'name': 'ZZ', 'age': 24, 'socre': 100}
print (pickle.dumps(d))

f = open ('test.txt', 'wb')
pickle.dump(d, f)
f.close

f = open ('test.txt', 'rb')
d = pickle.load(f)
f.close
print (d)

import json
d = {'name': 'ZZ', 'age': 24, 'socre': 100}
print(json.dumps(d))
json_str = '{"age": 24, "score": 100, "name": "Bob"}'
print (json.loads(json_str))
