#### 给函数添加元信息

```
def add(x: int, y: int) -> int:
    return x + y
help(add)
add.__annotations__
```

#### 返回多个值的函数

```
实际上 返回的是一个元祖
元祖的生成方式 有个语法
a = 1,2  # a是个元祖

def myfunc():
    return 1,2,3
# 因此  此函数返回的是一个元祖
```

#### 给函数默认值时,尽量给不可变对象

