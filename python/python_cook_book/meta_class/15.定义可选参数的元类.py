# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 定义一个元类，允许类定义时提供可选参数，这样可以控制或配置类型的创建过程

# 使用 ``metaclass``关键字参数来指定特定的元类。 例如使用抽象基类

from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass

# 为了使元类支持这些关键字参数，你必须确保在 __prepare__() , __new__() 和 __init__() 方法中 都使用强制关键字参数
class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # Custom processing
        pass
        return super().__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        pass
        return super().__new__(cls, name, bases, ns)

    # Required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        pass
        super().__init__(name, bases, ns)


# 在自定义元类中我们还可以提供其他的关键字参数
class Spam(metaclass=MyMeta, debug=True, synchronize=True):
    pass
