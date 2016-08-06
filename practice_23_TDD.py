class Dict (dict):
    def __init__ (self, **kw):
        super().__init__(**kw)

    def __getattr__ (self, key):
        try:
            return self[key]
        except:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__ (self, key, value):
        self[key] = value

d = Dict(a=1, b=2)
print (d['a'])
d1 = dict(a = 1, b =3)
print(d1)
d2 = {'a': 1, 'b' : 3}
print(d2)

import unittest

class TestDict (unittest.TestCase):

    def test_init (self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')#if 2 key value is equal
        self.assertTrue(isinstance(d, dict))#if it is super-class object

    def test_key (self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')# universal form test

    def test_attr (self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')# universal form test

    def test_keyerror (self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror (self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

if __name__ == '__main__':
    unittest.main()
