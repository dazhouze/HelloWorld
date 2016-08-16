'''
use 64 char to represent any byte file
'''
#3 bytes a group, re-group in 4 groups 3*8/4=6 bit = 64
import base64
print(base64.b64encode(b'binary\x00string'))
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))
print(base64.b64encode(b'hello world'))
