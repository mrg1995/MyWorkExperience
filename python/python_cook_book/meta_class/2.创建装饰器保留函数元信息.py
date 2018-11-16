# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 任何时候你定义装饰器的时候，都应该使用 functools 库中的 @wraps 装饰器来注解底层包装函数

import time
from functools import wraps
def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    print(n)

# @wraps 有一个重要特征是它能让你通过属性 __wrapped__ 直接访问被包装的函数
countdown.__wrapped__(100000)

if __name__ == '__main__':
    pass

