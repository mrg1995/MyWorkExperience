# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 在函数上添加一个包装器，增加额外的操作处理(比如日志、计时等)

# 使用装饰器

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    # @wraps(func)  会保留原始函数的元数据
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

if __name__ == '__main__':
    countdown(2)



