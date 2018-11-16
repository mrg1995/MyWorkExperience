# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 写一个装饰器，给函数添加日志功能，同时允许用户指定日志的级别和其他的选项。


from functools import wraps
import logging

# 最外层的函数 接受参数 并把那些参数作用在内部的装饰器函数上
def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

add(1,2)
spam()