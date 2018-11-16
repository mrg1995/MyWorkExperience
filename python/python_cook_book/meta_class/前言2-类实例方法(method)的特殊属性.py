# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


class A():

    def foo(self):
        '''a method'''
        print('hellow world!')

    bar = foo

    @classmethod
    def clsmtd(cls, arg):
        print(str(arg))


a = A()

'''
实例方法的只读属性
与自定义函数的特殊属性相比，实例方法具有 __self__,__func__ 这两个函数 所不具有的只读属性；此外，方法的 __doc__,__name__,__module__ 也是只读。对于实例方法而言，其 __self__ 属性为实例本身：

print(a.foo.__self__)
# <__main__.A object at 0x00000233DF6DE2E8>

print(a)
# <__main__.A object at 0x00000233DF6DE2E8>

而 __func__ 属性则返回方法所对应的底层函数：

print(a.foo)
# <bound method A.foo of <__main__.A object at 0x00000233DF6DE2E8>>
print(a.foo.__func__)  #注意与 a.foo 的区别
# <function A.foo at 0x00000233DF6C3F28>

至于 __doc__,__name__,__module__ 属性则与函数相应属性的值一致，所不同的是方法的这些属性均为只读，不可改写：

print(a.foo.__doc__)
# a method

print(a.foo.__name__)
# foo

print(a.foo.__module__)
# __main__
'''

'''
实例方法可通过底层函数访问函数属性
实例方法可以通过其底层的 function 对象（通过 __func__ 属性获得）访问函数所具有的特殊属性，如：

print(a.foo.__func__.__code__)
# <code object foo at 0x00000233DF6B5930, file "<ipython-input-43-c5636bcc492a>", line 3>
因此，诸如 __doc__,__name__,__module__等属性的值就可以通过底层函数相应的特殊属性进行改写：

a.foo.__doc__ = 'raise error'
# AttributeError: attribute '__doc__' of 'method' objects is not writable

print(a.foo.__func__.__doc__)
# a method
a.foo.__func__.__doc__ = 'can be changed through func doc'
print(a.foo.__doc__)
# can be changed through func doc


a.foo.__name__ = 'dobi'
# AttributeError: 'method' object has no attribute '__name__'

print(a.foo.__func__.__name__)
# foo
a.foo.__func__.__name__ = 'dobi'
print(a.foo.__name__)
# dobi
'''

'''
底层函数的唯一性
当一个类的实例方法是通过其他实例方法创建，则其他实例方法所对应的底层函数并非其所创建的实例方法，而是其所创建的实例方法所对应的底层函数：

print(a.bar) #注意这里 a.bar 是个实例方法
<bound method A.foo of <__main__.A object at 0x00000233DF6DE2E8>>
print(a.bar.__func__)
# <function A.foo at 0x00000233DF6C3F28>
上例中，通过其他实例方法 a.bar 创建了实例方法 a.foo，但a.bar.__func__ 却是 a.foo.__func__ 而非 a.foo：

print(a.foo.__func__)
# <function A.foo at 0x00000233DF6C3F28>
print(a.foo)
# <bound method A.foo of <__main__.A object at 0x00000233DF6DE2E8>>
'''

'''
实例方法的首位参数为实例本身
实例方法执行时，其底层函数的首位参数为实例本身,下面两行代码执行结果是一致的：

a.foo()
# hellow world!
a.foo.__func__(a)
# hellow world!
'''

'''
类实例方法的首位参数是类本身
当一个实例方法（严格来说是类实例方法）是由类方法创建，则其 __self__ 属性是其类本身：

print(a.clsmtd.__self__)
# <class '__main__.A'>
事实上，通过类方法建立的（类）实例方法，在调用底层函数时（下例是 A.clsmtd.__func__），其首位参数（也即 __self__）是类本身，这一点与实例方法执行时有所区别。

a.clsmtd('dog')
# dog
A.clsmtd('dog')
# dog
A.clsmtd.__func__(A, 'dog')
# dog
类实例方法，本身也是 bound method,这与实例方法一致：

print(a.clsmtd)
# <bound method A.clsmtd of <class '__main__.A'>>
print(a.foo)
# <bound method A.foo of <__main__.A object at 0x00000233DF6DE2E8>>
print(A.clsmtd)
# <bound method A.clsmtd of <class '__main__.A'>>
print(A.foo)
# <function A.foo at 0x00000233DF6C3F28>
一个是绑定类（类实例），另一个是绑定实例。
'''

'''
总结:
Python 3 有两种 bound method, 一种是 instance method,一种是 class method（class instance method）,两种都可以被实例访问；

对于 instance method 其 __self__ 属性值为 instance 本身，而 class method 其属性值则为 class 本身；

不管是 instance method 还是 class method ，执行时，都需要调用与之对应的底层函数（underlying function，通过 __func__ 访问）,底层函数的首位参数通过 __self__ 获得， 对于 instance method 其为该实例本身，对于 class method 则为该类本身；

bound method 可以通过对应的底层函数，访问函数的所有特殊属性。
'''
