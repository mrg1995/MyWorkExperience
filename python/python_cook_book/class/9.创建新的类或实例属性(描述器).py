# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 创建一个新的拥有一些额外功能的实例属性类型，比如类型检查

# 创建一个全新的实例属性，可以通过一个描述器类的形式来定义它的功能。

class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


# 一个描述器就是一个实现了三个核心的属性访问操作(get, set, delete)的类， 分别为 __get__() 、__set__() 和 __delete__() 这三个特殊的方法。 这些方法接受一个实例作为输入，之后相应的操作实例底层的字典。

# 使用一个描述器，需将这个描述器的实例作为类属性放到一个类的定义中
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
# 这样做后，所有对描述器属性(比如x或y)的访问会被 __get__() 、__set__() 和 __delete__() 方法捕获到。

# 描述器可实现大部分Python类特性中的底层魔法， 包括 @classmethod 、@staticmethod 、@property ，甚至是 __slots__ 特性


# 只是想简单的自定义某个类的单个属性访问的话就不用去写描述器了。 这种情况下使用property技术会更加容易。 当程序中有很多重复代码的时候描述器就很有用了 (比如你想在代码的很多地方使用描述器提供的功能或者将它作为一个函数库特性)。
