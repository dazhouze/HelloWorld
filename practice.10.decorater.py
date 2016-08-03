import functools
def log (text = None):
    def decorator (func):
        functools.wraps(func)
        def wraps (*argv, **kw):
            if text == None:
                print ("%s" % (func.__name__))
            else:
                print ("%s %s" % (text, func.__name__))
            return func(*argv, **kw)
        return wraps
    return decorator

@log ()
#@log ('excute')
def now ():
    print ('Aug 1 2016')

now()
print (now.__name__)

print ('partial function set a perticular factor for a new function')
int2 = functools.partial(int, base = 2)
print (int('10000'))
print (int('10000', base = 2))
print int2('10000')
