# 给函数增加额外的信息,这样使用者就能清楚这个函数怎么使用

# 使用函数参数注解

def add(x: int, y: int) -> int:
    return x + y


help(add)
# Help on function add in module __main__:
# add(x: int, y: int) -> int

# 函数注解 存储在 函数的 __annotations__ 属性中
add.__annotations__ # {'x': <class 'int'>, 'y': <class 'int'>, 'return': <class 'int'>}
