# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 在子类中调用父类的某个已经被覆盖的方法

# 使用 super() 函数

class A:
    def spam(self):
        print('A.spam')


class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # Call parent spam()


# super() 函数的一个常见用法是在 __init__() 方法中确保父类被正确的初始化了：
class A:
    def __init__(self):
        self.x = 0


class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

# __setattr__() 的实现包含一个名字检查。 如果某个属性名以下划线(_)开头，就通过 super() 调用原始的 __setattr__() ， 否则的话就委派给内部的代理对象 self._obj 去处理,就算没有显式的指明某个类的父类， super() 仍然可以有效的工作。
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value) # Call original __setattr__
        else:
            setattr(self._obj, name, value)


# 多继承顺序

# 子类会先于父类被检查
# 多个父类会根据它们在列表中的顺序被检查
# 如果对下一个类存在两个合法的选择，选择第一个父类
