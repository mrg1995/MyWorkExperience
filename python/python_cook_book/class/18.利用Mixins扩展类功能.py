# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 有很多有用的方法，想使用它们来扩展其他类的功能。但是这些类并没有任何继承的关系

# 某个库提供了一些基础类， 可以利用它们来构造你自己的类。

class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """
    __slots__ = ()  # 混入类都没有实例变量，因为直接实例化混入类没有任何意义

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    '''
    Only allow a key to be set once.
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)


class StringKeysMappingMixin:
    '''
    Restrict keys to strings only
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)
# DRF 中的viewset模块中有很多mixin
# mixin 混入类，有几点需要记住。
# 首先是，混入类不能直接被实例化使用。
# 其次，混入类没有自己的状态信息，也就是说它们并没有定义 __init__() 方法，并且没有实例属性。 这也是为什么我们在上面明确定义了 __slots__ = () 。
