#### fomat的骚操作

```python
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

# !r 格式化指明输出使用__repr__() 来代替默认的__str__()
print('p is {0!r}'.format(p))
```



#### 魔法函数 ____format____()

```python
#如果要一个实例 通过 format() 方法 得到一个格式化的输出
#需要在类中 自定义 __format__() 方法
_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
}
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
d = Date(2018, 11, 14)
format(d)  # 2018-11-14
format(d, 'mdy')  # 11/14/2018
```

#### 类中属性命名时 下划线的使用

```
大多数而言，你应该让你的非公共名称以单下划线开头。但是，如果你清楚你的代码会涉及到子类， 并且有些内部属性应该在子类中隐藏起来，那么才考虑使用双下划线方案。
```

#### property  属性方法

```python
# 可以通过这个  给 实例增加  访问和修改的处理逻辑 如 验证合法性
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
```

#### 描述器

```
只是想简单的自定义某个类的单个属性访问的话就不用去写描述器了。 这种情况下使用property技术会更加容易。 当程序中有很多重复代码的时候描述器就很有用了 (比如你想在代码的很多地方使用描述器提供的功能或者将它作为一个函数库特性)。
```

#### 简化数据结构的初始化

```
减少 写 仅作为数据结构的类 , 少写 __init__() 函数
```

#### 抽象基类 抽象方法


抽象基类只能继承而不能实例化，子类要实例化必须先覆写抽象基类中的抽象方法。
个人理解 : 有水果这个抽象基类，有苹果，香蕉，桃子类等，但你永远只能吃得到苹果，桃子这些，而不能吃到所谓的“水果”。


```
import abc
# 抽象类
# abstractmethod  指定了抽象方法  继承该抽象方法的子类在实例化时  会直接调用该抽象方法 如果没有复写 就会报错
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
```

#### 使用类方法构造初始化实例的方法

#### 设计模式 : 状态模式 

```
# 为每个状态定义一个对象
# 每个状态对象都只有静态方法，并没有存储任何的实例属性数据。 实际上，所有状态信息都只存储在 Connection 实例中

可以 减少if/else 判断语句 
```

####  通过字符串调用对象方法

```python
# 使用 getattr
getattr(p, 'distance')(0, 0)

# 使用operator
import operator
f = operator.methodcaller('distance', 0, 0)
f(p)
```

#### 设计模式 :访问者模式

```
对不同的对象 执行不同的方法
```

#### 创建缓存实例

```
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
```

