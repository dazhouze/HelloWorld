f = open('.gitignore', 'r')
con = f.read()
print (con)
f.close()

with open('.gitignore', 'r') as f1:# no need to use f.close()
    print (f1.read(5))
    print (f1.read(5))
    for line in f1.readlines():
        print (line.strip(), './././')

with open ('writeTest.txt', 'w') as f2:
    f2.write('hello world')

with open ('writeTest.txt', 'w') as f2:
    f2.write('hello china')
