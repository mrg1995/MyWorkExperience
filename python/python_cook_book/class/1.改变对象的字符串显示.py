# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


#  想改变对象实例的打印或显示输出，让它们更具可读性。

#  重新定义 它的 __str__() 和 __repr__() 方法即可

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)


p = Pair(1, 2)
p  # Pair(1, 2)
print(p)  # (1,2)

# !r 格式化指明输出使用__repr__() 来代替默认的__str__()
print('p is {0!r}'.format(p))

# 自定义 __repr__() 和 __str__() 是很好的习惯
# __repr__() 生成的文本字符串标准做法是需要让 eval(repr(x)) == x 为真
# 如果实在不能这样子做，应该创建一个有用的文本表示，并使用 < 和 > 括起来
# 如果 __str__() 没有被定义，那么就会使用 __repr__() 来代替输出。
