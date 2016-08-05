try:
    print ('try')
    r = 10/0
    print (r)
except ZeroDivisionError as e:
    print('except:', e)
except ValueError as e:
    print('except:', e)
else:
    print ('no error.')
finally:
    print('finally:')
print ('End')
print ('Python can capture error in high layer.')

class FooError (ValueError):
    pass

r = 0
if r == 0:
    pass
#    raise FooError('invaild value %d' % r)

r = 0
#assert r != 0, 'r should not be zero'

import logging
print ('logging level : debug info waring error.')
logging.basicConfig(level = logging.INFO)
if r == 0:
    logging.info('r = 0!')
