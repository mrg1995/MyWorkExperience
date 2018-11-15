# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 让某个类的实例支持标准的比较运算(比如>=,!=,<=,<等)，但是又不想去实现那一大丢的特殊方法。

# Python类对每个比较操作都需要实现一个特殊方法来支持。 例如为了支持>=操作符，你需要定义一个 __ge__() 方法。
# 尽管定义一个方法没什么问题，但如果要你实现所有可能的比较方法那就有点烦人了。

# 装饰器 functools.total_ordering 就是用来简化这个处理的。 使用它来装饰一个来，你只需定义一个 __eq__() 方法， 外加其他方法(__lt__, __le__, __gt__, or __ge__)中的一个即可。 然后装饰器会自动为你填充其它比较方法。

from functools import total_ordering

class Room:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(self.name,
                self.living_space_footage,
                self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage
