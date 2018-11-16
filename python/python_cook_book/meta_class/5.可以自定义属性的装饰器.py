# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 一个装饰器来包装一个函数，并且允许用户提供参数在运行时控制装饰器行为

#引入一个访问函数，使用 nonlocal 来修改内部变量。 然后这个访问函数被作为一个属性赋值给包装函数。

from functools import wraps, partial
import logging
# Utility decorator to attach a function as an attribute of obj

def attach_wrapper(obj, func=None):
    # 内部第一次 得到  obj 是 被装饰的函数
    if func is None:
        return partial(attach_wrapper, obj)
    # 第二次 是给 被装饰的函数添加 函数属性 也就是自定义装饰器属性的方法
    #通过 nonlocal 来控制修改函数内部的变量
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    '''
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y
'''
debug
decorate(add)

'''
@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

logging.basicConfig(level=logging.DEBUG)
add(1,2)
add.set_message('Add called')

'''
>>> logging.basicConfig(level=logging.DEBUG)
>>> add(2, 3)
DEBUG:__main__:add
5
>>> # Change the log message
>>> add.set_message('Add called')
>>> add(2, 3)
DEBUG:__main__:Add called
5
>>> # Change the log level
>>> add.set_level(logging.WARNING)
>>> add(2, 3)
WARNING:__main__:Add called
5
'''
