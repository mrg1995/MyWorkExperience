# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 使用一个装饰器去包装函数，但是希望返回一个可调用的实例。 需要让装饰器可以同时工作在类定义的内部和外部。

#  将装饰器定义成一个实例，需要确保它实现了 __call__() 和 __get__() 方法

import types
from functools import wraps

'''
def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)
    wrapper.ncalls = lambda: ncalls
    return wrapper

# Example
@profiled
def add(x, y):
    return x + y
'''


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


# 可以将它当做一个普通的装饰器来使用，在类里面或外面都可以
@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)

'''
执行时
>>> add(2, 3)
5
>>> add(4, 5)
9
>>> add.ncalls()
2
'''