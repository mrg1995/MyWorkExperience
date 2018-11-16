# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 想通过反省或重写 修改 类中某个方法  但是又不想继承 或 元类的方式

# 使用装饰器

# 下面是一个重写了特殊方法 __getattribute__ 的类装饰器， 可以打印日志：
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls


# Example use
@log_getattribute
class A:
    def __init__(self, x):
        self.x = x

    def spam(self):
        pass
