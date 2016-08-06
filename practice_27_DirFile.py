import os
print(os.name)
print(os.uname())
#print(os.environ)
print(os.environ.get('PATH'))

print(os.path.abspath('.'))
print(os.path.join('.', 'test'))
#os.rmdir('./test')
os.makedirs('./test')
os.rmdir('./test')
print(os.path.split('./test/test.txt'))
print(os.path.splitext('./test/test.txt'))

def dirl (path = '.'):
    for filename in os.listdir(path):
        print (os.path.getmtime(filename),'\t', os.path.getsize(filename), filename)

print (dirl())
