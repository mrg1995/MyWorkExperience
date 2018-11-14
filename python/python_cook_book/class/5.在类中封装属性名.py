# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 封装类的实例上面有“私有”数据，但是Python语言并没有访问控制。


# 遵循一定的属性和方法命名规约来达到这个效果。 第一个约定是任何以单下划线_开头的名字都应该是内部实现
# 使用下划线开头的约定同样适用于模块名和模块级别函数。


# 在类定义中使用两个下划线(__)开头的命名
# 面的类B中，私有属性会被分别重命名为 _B__private 和 _B__private_method
class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()


# 这种属性通过继承是无法被覆盖的
# 这里，私有名称 __private 和 __private_method 被重命名为 _C__private 和 _C__private_method ，这个跟父类B中的名称是完全不同
class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1  # Does not override B.__private

    # Does not override B.__private_method()
    def __private_method(self):
        pass

# 大多数而言，你应该让你的非公共名称以单下划线开头。但是，如果你清楚你的代码会涉及到子类， 并且有些内部属性应该在子类中隐藏起来，那么才考虑使用双下划线方案。
