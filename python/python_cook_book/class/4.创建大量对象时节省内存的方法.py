# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 要创建大量对象, 导致占用很大的内存

# 对于主要是用来当成简单的数据结构的类而言，你可以通过给类添加 __slots__ 属性来极大的减少实例所占的内存

class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

# 定义 __slots__ 后，Python就会为实例使用一种更加紧凑的内部表示
# 通过一个很小的固定大小的数组来构建，而不是为每个实例定义一个字典
#  使用slots后不能再给实例添加新的属性了，只能使用在 __slots__ 中定义的那些属性名。

# 定义了slots后的类不再支持一些普通类特性了，比如多继承
# 经常被使用到的用作数据结构的类上来 定义slots
# __slots__ 更多的是用来作为一个内存优化工具。