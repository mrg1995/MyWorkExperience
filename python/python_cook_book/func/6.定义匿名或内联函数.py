# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 比如 为 sort() 操作 创建一个很短的回调函数  不用def 写函数  而是以内联的方式来创建这个函数

# 匿名函数  lambda 表达式

add = lambda x, y: x + y
add(1, 2)

names = ['David Beazley', 'Brian Jones', 'Raymond Hettinger', 'Ned Batchelder']
# 以 名 进行排序
sorted(names, key=lambda name: name.split()[-1].lower())
# ['Ned Batchelder', 'David Beazley', 'Raymond Hettinger', 'Brian Jones']
