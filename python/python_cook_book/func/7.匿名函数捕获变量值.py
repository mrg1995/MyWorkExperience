# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 定义 匿名函数  并在定义时 捕获 到变量的值

x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

a(10)  # 30
b(10)  # 30
# 匿名函数 是在运行时绑定值的  所以 结果不是 20,30  而是30,30

# 如果 想让某个匿名函数 在定义时 就捕获绑定到值
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y

a(10) # 20
b(10) # 30