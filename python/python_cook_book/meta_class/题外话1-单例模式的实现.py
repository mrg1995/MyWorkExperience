# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 1 使用魔法函数 __new__

# 每次创建时 都是返回第一次创建时的实例
class BaseController(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = object.__new__(cls, *args, **kwargs)
        return cls._singleton


# 共享属性
class Borg(object):
    _state = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ == cls._state
        return obj


# 2 装饰器 实现
def singleton(cls):
    instances = {}

    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


# 3 import 方法
class My_Singleton(object):
    def foo(self):
        pass


my_singleton = My_Singleton()
# 直接调用这个实例  变相实现单例

# 4 使用魔法函数 __call__
class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


# Example
class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')
