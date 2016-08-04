# -*- coding: utf-8 -*-
print ('porperty is a decorator')
print ('练习')
class Screen (object):
    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__heigth

    @height.setter
    def height(self, value):
        self.__heigth = value

    @property
    def resolution(self):
        return self.__heigth * self.__width

# test:
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution
