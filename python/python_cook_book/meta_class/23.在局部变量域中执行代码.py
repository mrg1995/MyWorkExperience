# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 在使用范围内执行某个代码片段，并且希望在执行后所有的结果都不可见。

'''
>>> def test():
...     a = 13
...     loc = locals()
...     exec('b = a + 1')
...     b = loc['b']
...     print(b)
...
>>> test()
14
>>>
'''
