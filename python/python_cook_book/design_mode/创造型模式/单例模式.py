# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 保证一个类仅有一个实例，并提供一个访问它的全局访问点。


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass(object):
    __metaclass__ = Singleton
