# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 一个装饰器已经作用在一个函数上，想撤销它，直接访问原始的未包装的那个函数。

# 装饰器是通过 @wraps (参考第2个文件)来实现的,那么可以通过访问__wrapped__属性来访问原始函数


'''
>>> @somedecorator
>>> def add(x, y):
...     return x + y
...
>>> orig_add = add.__wrapped__
>>> orig_add(3, 4)
7
'''