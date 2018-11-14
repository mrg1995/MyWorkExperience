# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'


# 拓展函数中的某个闭包,允许它能访问和修改函数的内部变量

# 可以通过编写 访问方法 并将其作为 函数属性 绑定到闭包上来实现


def sample():
    n = 0

    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func


f = sample()
f()  # n=0
f.set_n(10)
f()  # n = 10
print(f.get_n())  # 10

# 在配置的时候给闭包添加方法会有更多的实用功能， 比如你需要重置内部状态、刷新缓冲区、清除缓存或其他的反馈机制的时候。