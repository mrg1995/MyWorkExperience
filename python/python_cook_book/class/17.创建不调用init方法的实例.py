# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 创建一个实例  但是希望绕过__init__()方法

# 可以通过 __new__() 方法 创建一个 未初始化的实例

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 创建一个未初始化的实例
d = Date.__new__(Date)
# 手动初始化
data = {'year': 2012, 'month': 8, 'day': 29}
for key, value in data.items():
    setattr(d, key, value)

from time import localtime
# 使用 类方法 和 __new__()  定义新的构造函数
class Date1:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):
        d = cls.__new__(cls)
        t = localtime()
        d.year = t.tm_year
        d.month = t.tm_mon
        d.day = t.tm_mday
        return d
