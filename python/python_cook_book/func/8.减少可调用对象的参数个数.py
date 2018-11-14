# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 有一个被其他python代码使用的callable对象，可能是一个回调函数或者是一个处理器， 但是它的参数太多了，导致调用时出错。

# 可以使用 functools.partial()  ,可以 给一个 或 多个 函数参数设置固定的值

from functools import partial


def spam(a, b, c, d):
    print(a, b, c, d)


s1 = partial(spam, 1, d=1)

s1(2, 3)  # 1 2 3 1

# partial() 固定某些参数 并返回一个新的 callable对象  这个对象接收未赋值的参数 然后 和已经赋值过的参数拼接起来
