# 函数的某些参数强制使用关键字参数传递

# 将强制关键字参数放到某个*参数 或者单个 * 后面就能达到这个效果

def recv(maxsize, *, block):
    'Receives a message'
    pass


recv(1024, True)  # TypeError
recv(1024, block=True)  # Ok


# 利用这种技术  可以接受任意多个位置参数的函数中指定关键字参数
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m


minimum(1, 5, 2, -5, 10)  # Returns -5
minimum(1, 5, 2, -5, 10, clip=0)  # Returns 0
