# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 利用 魔法函数 __call__
class A:
    def __call__(self, *args, **kwargs):
        print('我是call')


a = A()
print(callable(a))  # True
a()  # 我是call


# __call__ 方法 在每次调用实例对象时 都会 实现 __call__方法

# 结合类的特性来说，类可以记录数据（属性），而函数不行（闭包某种意义上也可行），利用这种特性可以实现基于类的装饰器，在类里面记录状态

class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


# 经过这个装饰器  foo 函数实际上已经变成了 count 的实例了
# 因为装饰的过程  就是  foo = Counter(foo)
@Counter
def foo():
    pass


# for循环调用时  每次都会实现__call__ 方法
for i in range(10):
    foo()

print(foo.count)  # 10
