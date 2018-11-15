# -*- coding:utf-8 -*-
import math
import abc

__author__ = 'xiaodong Guo'

# 实例方法
# 实例方法的定义只需要把第一个参数指定为 self，尽管这个名字可以是任意取的，但约定俗成为 self，该参数就是该类的一个实例对象
'''
>>> class Pizza(object):
...     def __init__(self, size):
...         self.size = size
...     def get_size(self):
...         return self.size
...
>>> Pizza.get_size
<function Pizza.get_size at 0x7f307f984dd0>
'''


# 静态方法  @staticmethod
# 有时可能需要写一个属于这个类的方法，但是这些代码不会使用到实例对象本身
class Pizza(object):
    def __init__(self):
        pass

    @staticmethod
    def mix_ingredients(x, y):
        return x + y

    def cook(self):
        return self.mix_ingredients(self.cheese, self.vegetables)


# 类方法 @classmethod
# 类方法不是绑定在实例上的 而是绑定在类上的方法
# 两种场景 会经常使用到 类方法
# 1 工厂函数  用于创建类的实例
class Pizza1(object):
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def from_fridge(cls, fridge):
        return cls(fridge.get_cheese() + fridge.get_vegetables())


# 2 通过 类方法来调用静态方法
class Pizza2(object):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    @staticmethod
    def compute_area(radius):
        return math.pi * (radius ** 2)

    @classmethod
    def compute_volume(cls, height, radius):
        return height * cls.compute_area(radius)

    def get_volume(self):
        return self.compute_volume(self.height, self.radius)


# 抽象方法
# 抽象方法是定义在基类中的一种方法，它没有提供任何实现

# 因为抽象基类只能继承而不能实例化，子类要实例化必须先覆写抽象基类中的抽象方法。
# 个人理解 : 有水果这个抽象基类，有苹果，香蕉，桃子类等，但你永远只能吃得到苹果，桃子这些，而不能吃到所谓的“水果”。

# 抽象类的目的就是让别的类继承它并实现特定的抽象方法

# 抽象类
# abstractmethod  是 指定抽象方法  子类 在实例化实例时  会直接调用该抽象方法
class Foo(abc.ABC):
    @abc.abstractmethod
    def fun(self):
        pass


# 具体实现类
class Sub_foo(Foo):
    def f(self):
        print('This is sub foo!')

    def fun(self):
        print('This is sub foo!')


# 抽象基类的另一个主要用途是在代码中检查某些类是否为特定类型，实现了特定接口
'''
def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')
    pass
'''


# 混合 抽象方法, 静态方法, 类方法

class BasePizza(object):
    __metaclass__ = abc.ABCMeta

    default_ingredients = ['cheese']

    # 不能强制抽象方法的实现是一个常规方法、或者是类方法还是静态方法,这里仅仅只是抽象类的类方法
    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
        """Returns the ingredient list."""
        return cls.default_ingredients


class DietPizza(BasePizza):
    def get_ingredients(self):
        return ['egg'] + super(DietPizza, self).get_ingredients()


if __name__ == '__main__':
    # a = Foo()
    c = Sub_foo()
