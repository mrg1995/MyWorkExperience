# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 给实例 属性 增加 除访问和修改的其他处理逻辑,如类型检查或合法性验证

# 自定义某个属性的一种简单方法是将它定义为一个property  属性方法

class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


# property的一个关键特征是它看上去跟普通的attribute没什么两样， 但是访问它的时候会自动触发 getter 、setter 和 deleter 方法
# Properties还是一种定义动态计算attribute的方法。 这种类型的attributes并不会被实际的存储，而是在需要的时候计算出来。

import math
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius
