from io import StringIO
f = StringIO()
f.write('hello')
f.write('\t')
f.write('world')
#print (f)
print ( f.getvalue())

from io import BytesIO
fb = BytesIO()
fb.write('中文'.encode('utf-8'))
print(fb.getvalue())
