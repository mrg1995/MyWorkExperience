# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'



import weakref

class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# Example
class Spam(metaclass=Cached):
    def __init__(self, name):
        print('Creating Spam({!r})'.format(name))
        self.name = name


if __name__ == '__main__':
    a = Spam("gui")
    b = Spam("xixi")
    c = Spam("gui")
    print(a is c)