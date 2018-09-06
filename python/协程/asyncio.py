# import paho.mqtt.publish as publish
#
# HOST = "127.0.0.1"
#
# publish.single("lettuce", "payload", hostname=HOST, port=1883,
#                auth={'username': "admin", 'password':"password"})


import asyncio


# 定义协程
async def do_some_work(x):
    print("Waiting " + str(x))
    #  asyncio.sleep(x) 睡眠几秒 模拟实际工作
    await asyncio.sleep(x)
    return 2


# 判断是否是协程函数
print(asyncio.iscoroutinefunction(do_some_work))
# 判断是否是协程对象  (这里会报警告)
print(asyncio.iscoroutine(do_some_work(3)))

# 运行协程
loop = asyncio.get_event_loop()
# run_until_complete函数是个阻塞调用,直到协程运行结束,
# 参数是 一个future   但是我们这里传入的是协程对象
# 之所以可以这样 是因为run_until_complete函数 内部做了检查  已经做了处理: 用ensure_future函数将协程对象包装成future
loop.run_until_complete(do_some_work(3))
# 因此也可以这样写
loop.run_until_complete(asyncio.ensure_future(do_some_work(3)))


# 回调
def done_callback(futu):
    print("done")
    # 可以使用协程的响应  这里为2
    print(futu._result)
# 创建任务   task  (与future 一样)
futu = asyncio.ensure_future(do_some_work(3))
# 添加回调函数
futu.add_done_callback(done_callback)
# 执行协程
loop.run_until_complete(futu)


# 多个协程
# 使用 gather 函数
loop.run_until_complete(asyncio.gather(do_some_work(1), do_some_work(3)))
# 也可以把协程放到列表中
coros = [do_some_work(1), do_some_work(3)]
loop.run_until_complete(asyncio.gather(*coros))
# loop.run_until_complete 函数只接受单个future  所以需要gather函数把多个future包装成单个future


# run_until_complete 和 run_forever
# run_until_complete 是协程运行完 就返回了
# run_forever 是协程运行完  程序也不退出 直到stop被调用
# run_forever 一般不怎么会用到  run_until_complete内部实际上调用的是run_forever

# 调用loop.close
# 只要loop不关闭  就能再运行
# loop.run_until_complete(do_some_work(1))
# loop.run_until_complete(do_some_work(3))
# loop.close()

# 一般在调用完loop后就调用 loop.close  彻底清理loop对象 防止误用
loop.run_until_complete(do_some_work(1))
loop.close()
# 上面关闭了  就不能再运行了
loop.run_until_complete(do_some_work(3))

# gather 和 wait 的不同
# 功能类似  不过wait可以放入协程列表
coros = [do_some_work(1), do_some_work(3)]
loop.run_until_complete(asyncio.wait(coros))













