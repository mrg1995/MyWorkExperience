# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 对函数参数进行强制类型检查

#  目标是 能对函数参数类型进行断言
'''
>>> @typeassert(int, int)
... def add(x, y):
...     return x + y
...
>>> add(2, 3)
5
>>> add(2, 'hello')
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "contract.py", line 33, in wrapper
TypeError: Argument y must be <class 'int'>
'''

from inspect import signature
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func
        # Map function argument names to supplied types
        # 类型到名称的部分绑定
        # sig.bind_partial().argument  返回一个字典
        # OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)])
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # bound_values.arguments 返回的是 所有 的 名称及数值
            # OrderedDict([('x', 1), ('y', 2), ('z', 3)])
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)

        return wrapper

    return decorate


@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)


spam(1, 2, 3)
spam(1, 2, 'world')

# inspect 模块中可以找到更多关于函数参数对象的信息