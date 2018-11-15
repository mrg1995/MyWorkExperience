# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 定义一个接口或抽象类，并且通过执行类型检查来确保子类实现了某些特定的方法

# 使用 abc 模块 定义抽象基类

from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass
# 抽象类的一个特点是它不能直接被实例化

# 标准库中有很多用到抽象基类的地方。collections 模块定义了很多跟容器和迭代器(序列、映射、集合等)有关的抽象基类。 numbers 库定义了跟数字对象(整数、浮点数、有理数等)有关的基类。io 库定义了很多跟I/O操作相关的基类。
import collections
'''
# Check if x is a sequence
if isinstance(x, collections.Sequence):


# Check if x is iterable
if isinstance(x, collections.Iterable):


# Check if x has a size
if isinstance(x, collections.Sized):


# Check if x is a mapping
if isinstance(x, collections.Mapping):
'''
