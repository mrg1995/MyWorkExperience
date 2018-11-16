# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'

# 构造和初始化
'''
__init__我们很熟悉了,它在对象初始化的时候调用,我们一般将它理解为"构造函数".

实际上, 当我们调用x = SomeClass()的时候调用,__init__并不是第一个执行的, __new__才是。所以准确来说,是__new__和__init__共同构成了"构造函数".

__new__是用来创建类并返回这个类的实例, 而__init__只是将传入的参数来初始化该实例.

__new__在创建一个实例的过程中必定会被调用,但__init__就不一定，比如通过pickle.load的方式反序列化一个实例时就不会调用__init__。

__new__方法总是需要返回该类的一个实例，而__init__不能返回除了None的任何值。比如下面例子:

class Foo(object):

    def __init__(self):
        print 'foo __init__'
        return None  # 必须返回None,否则抛TypeError

    def __del__(self):
        print 'foo __del__'
        
实际中,你很少会用到__new__，除非你希望能够控制类的创建。
如果要讲解__new__，往往需要牵扯到metaclass(元类)的介绍。

对于__new__的重载，Python文档中也有了详细的介绍。

在对象的生命周期结束时, __del__会被调用,可以将__del__理解为"析构函数".
__del__定义的是当一个对象进行垃圾回收时候的行为。

有一点容易被人误解, 实际上，x.__del__() 并不是对于del x的实现,但是往往执行del x时会调用x.__del__().

怎么来理解这句话呢? 继续用上面的Foo类的代码为例:

foo = Foo()
foo.__del__()
print foo
del foo
print foo  # NameError, foo is not defined
如果调用了foo.__del__()，对象本身仍然存在. 但是调用了del foo, 就再也没有foo这个对象了.

请注意，如果解释器退出的时候对象还存在，就不能保证 __del__ 被确切的执行了。所以__del__并不能替代良好的编程习惯。
比如，在处理socket时，及时关闭结束的连接
'''

# 属性访问控制
'''
总有人要吐槽Python缺少对于类的封装,比如希望Python能够定义私有属性，然后提供公共可访问的getter和 setter。Python其实可以通过魔术方法来实现封装。

__getattr__(self, name)
该方法定义了你试图访问一个不存在的属性时的行为。因此，重载该方法可以实现捕获错误拼写然后进行重定向, 或者对一些废弃的属性进行警告。

__setattr__(self, name, value)
__setattr__ 是实现封装的解决方案，它定义了你对属性进行赋值和修改操作时的行为。
不管对象的某个属性是否存在,它都允许你为该属性进行赋值,因此你可以为属性的值进行自定义操作。有一点需要注意，实现__setattr__时要避免"无限递归"的错误，下面的代码示例中会提到。

__delattr__(self, name)
__delattr__与__setattr__很像，只是它定义的是你删除属性时的行为。实现__delattr__是同时要避免"无限递归"的错误。

__getattribute__(self, name)
__getattribute__定义了你的属性被访问时的行为，相比较，__getattr__只有该属性不存在时才会起作用。
因此，在支持__getattribute__的Python版本,调用__getattr__前必定会调用 __getattribute__。__getattribute__同样要避免"无限递归"的错误。
需要提醒的是，最好不要尝试去实现__getattribute__,因为很少见到这种做法，而且很容易出bug。

例子说明__setattr__的无限递归错误:

def __setattr__(self, name, value):
    self.name = value
    # 每一次属性赋值时, __setattr__都会被调用，因此不断调用自身导致无限递归了。

因此正确的写法应该是:
def __setattr__(self, name, value):
    self.__dict__[name] = value

__delattr__如果在其实现中出现del self.name 这样的代码也会出现"无限递归"错误，这是一样的原因。

下面的例子很好的说明了上面介绍的4个魔术方法的调用情况:

class Access(object):

    def __getattr__(self, name):
        print '__getattr__'
        return super(Access, self).__getattr__(name)

    def __setattr__(self, name, value):
        print '__setattr__'
        return super(Access, self).__setattr__(name, value)

    def __delattr__(self, name):
        print '__delattr__'
        return super(Access, self).__delattr__(name)

    def __getattribute__(self, name):
        print '__getattribute__'
        return super(Access, self).__getattribute__(name)

access = Access()
access.attr1 = True  # __setattr__调用
access.attr1  # 属性存在,只有__getattribute__调用
try:
    access.attr2  # 属性不存在, 先调用__getattribute__, 后调用__getattr__
except AttributeError:
'''

# 描述器对象
'''
我们从一个例子来入手,介绍什么是描述符,并介绍__get__, __set__, __delete__ 的使用。(放在这里介绍是为了跟上一小节介绍的魔术方法作对比)

我们知道，距离既可以用单位"米"表示,也可以用单位"英尺"表示。
现在我们定义一个类来表示距离,它有两个属性: 米和英尺。

class Meter(object):
    ''Descriptor for a meter.''
    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)

class Foot(object):
    def __get__(self, instance, owner):
        return instance.meter * 3.2808
    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808

class Distance(object):
    meter = Meter()
    foot = Foot()

d = Distance()
print d.meter, d.foot  # 0.0, 0.0
d.meter = 1
print d.meter, d.foot  # 1.0 3.2808
d.meter = 2
print d.meter, d.foot  # 2.0 6.5616

在上面例子中,在还没有对Distance的实例赋值前, 我们认为meter和foot应该是各自类的实例对象, 但是输出却是数值。这是因为__get__发挥了作用.

我们只是修改了meter,并且将其赋值成为int，但foot也修改了。这是__set__发挥了作用.

描述器对象(Meter、Foot)不能独立存在, 它需要被另一个所有者类(Distance)所持有。
描述器对象可以访问到其拥有者实例的属性，比如例子中Foot的instance.meter。

在面向对象编程时，如果一个类的属性有相互依赖的关系时，使用描述器来编写代码可以很巧妙的组织逻辑。
在Django的ORM中, models.Model中的IntegerField等, 就是通过描述器来实现功能的。

一个类要成为描述器，必须实现__get__, __set__, __delete__ 中的至少一个方法。下面简单介绍下:

__get__(self, instance, owner)

参数instance是拥有者类的实例。参数owner是拥有者类本身。__get__在其拥有者对其读值的时候调用。

__set__(self, instance, value)

__set__在其拥有者对其进行修改值的时候调用。

__delete__(self, instance)

__delete__在其拥有者对其进行删除的时候调用。
'''


# 其他 魔术方法  可在 https://segmentfault.com/a/1190000007256392 查看


