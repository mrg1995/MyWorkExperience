# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 在装饰器中给被包装函数增加额外的参数，但是不能影响这个函数现有的调用规则。

# 使用关键字参数来给被包装函数增加额外参数

from functools import wraps
# 普通版本 但是如果 函数中也有debug关键字参数的话 就会有问题
def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    return wrapper

'''
>>> @optional_debug
... def spam(a,b,c):
...     print(a,b,c)
...
>>> spam(1,2,3)
1 2 3
>>> spam(1,2,3, debug=True)
Calling spam
1 2 3
'''

import inspect
# 升级版 把 关键字先过滤一下  并把 关键字 加入到被包装函数的签名中
def optional_debug1(func):
    if 'debug' in inspect.getfullargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter('debug',
                inspect.Parameter.KEYWORD_ONLY,
                default=False))
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper
