# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 有一个字符串形式的方法名称，想通过它调用某个对象的对应方法。

# 1 使用 getattr()
# 通过 getattr() 来查找到这个属性，然后再去以函数方式调用它即可
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:},{!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)


p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)  # Calls p.distance(0, 0)

# 2  使用 operator.methodcaller()
# operator.methodcaller() 创建一个可调用对象，并同时提供所有必要参数， 然后调用的时候只需要将实例对象传递给它即可
import operator

f = operator.methodcaller('distance', 0, 0)
f(p)
# operator.methodcaller('distance', 0, 0)(p)
