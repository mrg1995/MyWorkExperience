# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# python 中 function 和 method的区别
class C(object):
    def foo(self):
        print(self)


# 需要明确传递参数的是function，不需要明确传递参数的是method。
# 类直接调用是function，类的实例调用的是method
'''
C.foo(1)  # 1
C().foo()  # <__main__.C object at 0x0000024B1FA2D780>
C.foo.__class__  # function
C().foo.__class__  # method
'''


# 这里介绍的是自定义函数（function类型）的特殊属性，而非方法（method 类型）的特殊属性
class Test():
    def func(self, v='dog'):
        '''这里演示一个闭包函数'''
        name = 'dobi'

        def inn_func(age=1):
            print(name, v, age)

        return inn_func


test = Test()
clsfunc = test.func()

'''
__doc__
可写；用于获取函数的文档说明，如果没有，则返回 None。

print('Test.func.__doc__:', Test.func.__doc__)
# Test.func.__doc__: 这里演示一个闭包函数

Test.func.__doc__ = 'ddd'  #注意，这里是 Test,不能是 test
print('Test.func.__doc__:', Test.func.__doc__)
# Test.func.__doc__: ddd
'''

'''
__name__
可写；获取函数的名称。

print('Test.func.__name__:', Test.func.__name__)
# Test.func.__name__: func

Test.func.__name__ = 'pet'
print('Test.func.__name__:', Test.func.__name__)
# Test.func.__name__: pet
'''

'''
__qualname__
可写；获取函数的qualname：点示法显示函数名称、所在的类、模块等梯级地址。

print('Test.func.__qualname__:', Test.func.__qualname__)
# Test.func.__qualname__: Test.func

Test.func.__qualname__ = 'path'
print('Test.func.__qualname__:', Test.func.__qualname__)
# Test.func.__qualname__: path
'''

'''
__module__
可写；返回函数所在的模块，如果无则返回None。

print('Test.func.__module__:', Test.func.__module__)
# Test.func.__module__: __main__

Test.func.__module__ = 'a'
print('Test.func.__module__:', Test.func.__module__)
# Test.func.__module__: a
'''

'''
__defaults__
可写；以元组的形式返回函数的默认参数，如果无默认参数则返回None。

print('Test.func.__defaults__:', Test.func.__defaults__)
# Test.func.__defaults__: ('dog',)

Test.func.__defaults__ = ('cat',)
print('Test.func.__defaults__:', Test.func.__defaults__)
# Test.func.__defaults__: ('cat',)

print('clsfunc.__defaults__:', clsfunc.__defaults__)
# clsfunc.__defaults__: (1,)

clsfunc.__defaults__ = (2,)
print('clsfunc.__defaults__:', clsfunc.__defaults__)
# clsfunc.__defaults__: (2,)
'''

'''
__code__
可写；返回已编译的函数对象。

print('Test.func.__code__:', Test.func.__code__)
# Test.func.__code__: <code object func at 0x0000020F072C2F60, file "D:\...\a.py", line 4>

def func2():print('cat')
Test.func.__code__ = func2.__code__
Test.func()
# cat

print('Test.func.__code__:', Test.func.__code__)
# Test.func.__code__: <code object func2 at 0x0000020F072C5780, file "D:\...\a.py", line 38>
'''

'''
__globals__
只读，以字典的形式返回函数所在的全局命名空间所定义的全局变量。

print('Test.func.__globals__:', Test.func.__globals__)
# Test.func.__globals__: {
# '__cached__': None, 
# 'Test': <class '__main__.Test'>, 
# '__builtins__': <module 'builtins' (built-in)>, 
# 'func2': <function func2 at 0x0000020F077D3C80>, 
# '__spec__': None, 
# '__doc__': None, 
# '__file__': 'D:\\...\\a.py', 
# 'test': <__main__.Test object at 0x0000020F077E5DA0>, 
# 'clsfunc': <function Test.func.<locals>.inn_func at 0x0000020F071D7F28>, 
# '__package__': None, 
# '__name__': '__main__', 
# '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x0000020F07289828>
# }
'''

'''
__dict__
可写；以字典的形式返回命名空间所支持的任意自定义的函数属性。

print('Test.func.__dict__:', Test.func.__dict__)
# Test.func.__dict__: {}
'''

'''
__closure__
只读；以包含cell的元组形式返回闭包所包含的自由变量。

print('Test.func.__closure__:', Test.func.__closure__)
# None

print('clsfunc.__closure__:', clsfunc.__closure__)
# clsfunc.__closure__: (
# <cell at 0x0000020F071FE708: str object at 0x0000020F07289998>, 
# <cell at 0x0000020F072B8C78: str object at 0x0000020F0766C538>
# )

print('clsfunc.__closure__[x]:', clsfunc.__closure__[0].cell_contents, clsfunc.__closure__[1].cell_contents)
# clsfunc.__closure__[x]: dobi dog
'''

'''
__annotations__
函数注释
def dog(name:str, age:(1, 99), species:'狗狗的品种') -> tuple:
    return (name, age, species)

dog.__annotations__
# {'age': (1, 99), 'name': str, 'return': tuple, 'species': '狗狗的品种'}
'''

'''
__kwdefaults__
强制关键字参数
'''
