#### 创建装饰器保留函数元信息

```python
# 任何时候你定义装饰器的时候，都应该使用 functools 库中的 @wraps 装饰器来注解底层包装函数
import time
from functools import wraps
def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper
 @timethis
def countdown(n):
    print(n)
# @wraps 有一个重要特征是它能让你通过属性 __wrapped__ 直接访问被包装的函数
countdown.__wrapped__(100000) 
```

#### 定义带参数的装饰器

```python
# 最外层的函数 接受参数 并把那些参数作用在内部的装饰器函数上
def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate
```

#### 可以自定义参数的装饰器

​	可以直接在业务逻辑中,修改装饰器的配置,从而控制被包装函数的行为

#### 带可选参数的装饰器

​	装饰器可以不带参数  也可以带参数

#### 利用装饰器强制函数上的类型检查

```python
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func
        # Map function argument names to supplied types
        # 类型到名称的部分绑定
        # sig.bind_partial().argument  返回一个字典
        # OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)])
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # bound_values.arguments 返回的是 所有 的 名称及数值
            # OrderedDict([('x', 1), ('y', 2), ('z', 3)])
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)

        return wrapper

    return decorate
```

```python
@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)
```

#### 装饰器类

```python
# 将装饰器定义成一个实例，需要确保它实现了 __call__() 和 __get__() 方法
class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
# 可以将它当做一个普通的装饰器来使用，在类里面或外面都可以
@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)
'''
执行时
>>> add(2, 3)
5
>>> add(4, 5)
9
>>> add.ncalls()
2
'''
```

#### 装饰器为被包装的函数提供额外参数



