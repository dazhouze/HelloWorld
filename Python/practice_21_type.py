print ('type() function is used to figure out object type.')
class Hello (object):
    def hello (self, name = 'world'):
        print ('hello %s' % name)

h1 = Hello()
h1.hello()
h1.hello('China')
print (type(Hello))
print ('The type of class is type.')
print (type(h1))


print ('type creat class.')
def fn (self, name = 'you'):
    print ('See %s' % name)
Bye = type('GoodBye', (object,), dict(GoodBye = fn))
b1 = Bye()
b1.GoodBye()

print('metaclass def first, then class , then instance.')


