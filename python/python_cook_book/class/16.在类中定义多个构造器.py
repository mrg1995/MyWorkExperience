# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 一个类 除了 __init__() 方法  其他初始化实例的方法

import time

class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)
'''
# 直接调用类方法创建实例
a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate
'''


