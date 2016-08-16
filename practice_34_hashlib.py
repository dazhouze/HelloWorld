'''
md5 SHA1
'''
import hashlib
md5 = hashlib.md5()
md5.update('hello world - by Ze'.encode('utf-8'))
print (md5.hexdigest())

md5.update('hello world, hellow China - by Ze'.encode('utf-8'))
print (md5.hexdigest())
