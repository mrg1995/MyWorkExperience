# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 在创建一个类的对象时，如果之前使用同样参数创建过这个对象， 直接返回它的缓存引用。

# 类似于 logging 模块  相同参数创建的对象是单例的
import weakref


# The class in question
# 管理器类
class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            temp = Spam._new(name)  # Modified creation
            self._cache[name] = temp
        else:
            temp = self._cache[name]
        return temp

    def clear(self):
        self._cache.clear()


# 不允许直接实例化 spam类 必须使用管理器生成实例
class Spam:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Can't instantiate directly")

    # Alternate constructor
    # 自定义实例生成方法
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        return self


if __name__ == '__main__':
    pool = CachedSpamManager()
    spam1 = pool.get_spam('1')
    spam2 = pool.get_spam('2')
    spam3 = pool.get_spam('1')
    print(spam1 is spam3)  # True
# Caching support
# The class in question
'''
class Spam:
    def __init__(self, name):
        self.name = name
# 创建弱引用池
_spam_cache = weakref.WeakValueDictionary()
# 每次生成实例时  先去 引用池中查找实例  若没有 则新建实例
def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s
'''
