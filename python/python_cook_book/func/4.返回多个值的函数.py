# 构造一个可以返回多个值的函数

# 可以直接返回一个元祖

def myfunc():
    return 1,2,3

a, b, c = myfunc()

# 尽管看起来返回了3个值  实际上 先创建了一个元祖  然后返回
# 这个语法比较奇怪  实际上使用 逗号 , 生成元祖的

d = 1,2
print(d)  # (1, 2)

