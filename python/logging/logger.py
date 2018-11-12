import logging
import os
import logging.handlers

'''
%(name)s  Logger的名字
%(levelno)s  数字形式的日志级别
%(levelname)s  文本形式的日志级别
%(pathname)s  调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s 用户输出的消息
'''
'''
# 直接调用
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/tmp/test.log',
                    filemode='w')
 
logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
'''
# Logger
# logger是个树形层级结构

# 如果未写名字 则获取默认的logger
# 获得实例
logger = logging.getLogger("base")
# 设置日志级别
logger.setLevel(logging.INFO)

# Handler
'''
logging.StreamHandler 可以向类似与sys.stdout或者sys.stderr的任何文件对象(file object)输出信息
logging.FileHandler 用于向一个文件输出日志信息
logging.handlers.RotatingFileHandler 类似于上面的FileHandler，但是它可以管理文件大小。当文件达到一定大小之后，它会自动将当前日志文件改名，然后创建一个新的同名日志文件继续输出
logging.handlers.TimedRotatingFileHandler 和RotatingFileHandler类似，不过，它没有通过判断文件大小来决定何时重新创建日志文件，而是间隔一定时间就自动创建新的日志文件
logging.handlers.SocketHandler 使用TCP协议，将日志信息发送到网络。
logging.handlers.DatagramHandler 使用UDP协议，将日志信息发送到网络。
logging.handlers.SysLogHandler 日志输出到syslog
logging.handlers.NTEventLogHandler 远程输出日志到Windows NT/2000/XP的事件日志 
logging.handlers.SMTPHandler 远程输出日志到邮件地址
logging.handlers.MemoryHandler 日志输出到内存中的制定buffer
logging.handlers.HTTPHandler 通过"GET"或"POST"远程输出到HTTP服务器
'''
# 向文件输出的管理器
fh = logging.FileHandler("./test.log")
# 向控制台输出的管理器
ch = logging.StreamHandler()

# 给管理器设置 日志等级
fh.setLevel(logging.DEBUG)
# Formatter
# 给管理器添加 格式化样式
formatter = logging.Formatter('%(name)s %(asctime)s %(filename)s[line:%(lineno)d] '
                   '%(levelname)s %(message)s')
fh.setFormatter(formatter)

# filter
# 给管理器添加 过滤器
# 只有满足  a.b.c 的logger 才会有输出
'''
filter = logging.Filter('mylogger.child1')
fh.addFilter(filter)
'''

# logger添加 管理器实例
# logger.addHandler(fh)
# logger.addHandler(ch)

handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(os.path.dirname(__file__),
                          '{name}.txt'.format(name="name")),  # 输出文件名
    maxBytes=1024 * 1024 * 5,  # 一个日志文件的大小上限 5m
    backupCount=5,  # 日志文件个数
    mode='a',  # 写日志模式
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.warning('111')