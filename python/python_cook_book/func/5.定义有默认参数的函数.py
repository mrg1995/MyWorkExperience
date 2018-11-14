# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 定义一个 函数 有一个或多个 参数 是可选的 并且有一个默认值

# 直接在函数定义中给参数指定一个默认值,并放到参数列表最后即可

def spam(a, b=42):
    print(a, b)

spam(1) #  a=1, b=42
spam(1, 2) # . a=1, b=2

# 如果并不想提供一个默认值,只是想测试下某个默认参数有没传递进来
# object 是所有类的基类 创建的实例没有任何用处  唯一作用就是测试同一性
_no_value = object()
def sppam(a, b=_no_value):
    if b is _no_value:
        raise ('No b value supplied')


# 默认值一般是不可变对象
# 如果一定要 可修改的容器 如 列表 集合 或者 字典
def spam(a, b=None):
    if b is None:
        b = []
