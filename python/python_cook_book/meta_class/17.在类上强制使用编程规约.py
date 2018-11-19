# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 程序包含一个很大的类继承体系，希望强制执行某些编程规约（或者代码诊断）来帮助程序员保持清醒。

# 想监控类的定义，通常可以通过定义一个元类。一个基本元类通常是继承自 type 并重定义它的 __new__() 方法 或者是 __init__() 方法

# 使用这个元类，通常要将它放到到一个顶级父类定义中，然后其他的类继承这个顶级父类。
class NoMixedCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('Bad attribute name: ' + name)
        return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self): # Ok
        pass

class B(Root):
    def fooBar(self): # TypeError
        pass

