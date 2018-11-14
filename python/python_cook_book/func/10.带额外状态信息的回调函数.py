# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 代码中需要依赖到回调函数的使用(比如事件处理器、等待后台任务完成后的回调等)， 并且你还需要让回调函数拥有额外的状态值，以便在它的内部使用到

# 这种情况 出现在很多函数库和框架中的回调函数的使用——特别是跟异步处理有关的。

def add(x,y):
    return x + y

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


# 这段代码可以加一些更高级的处理  包括 线程 进程 定时器等
# 这里只关注回调函数的调用,让回调函数访问外部信息,不仅仅只有 一个result 参数,加上状态信息等

# 1. 通过类绑定 信息来实现
class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add,(1,2),callback=r.handler)  # [1] Got: 3
apply_async(add, ('hello', 'world'), callback=r.handler) # [2] Got: helloworld

# 2 通过闭包 来捕捉状态值
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler
handler1 = make_handler()
apply_async(add,(1,2),callback=handler1)# [1] Got: 3
apply_async(add, ('hello', 'world'), callback=handler1)# [2] Got: helloworld

