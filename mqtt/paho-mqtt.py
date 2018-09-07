# 回调函数

def on_connect(client, userdata, flags, rc):
    '''
     当代理响应连接请求时调用
    :param client: 调用回调函数的客户端实例
    :param userdata: 创建客户端实例时设置 或者使用 client.user_data_set() 进行设置
    :param flags: 一个包含代理回复标志的字典
    :param rc: 值决定了连接的成功与否 为0-5
    :return:
    '''
    print("connected with result code {}".format(rc))
    client.subscribe("lettuce")


def on_disconnect(client, userdata, rc):
    '''
    当与代理断开连接时调用
    :param client:  客户端实例
    :param userdata:
    :param rc:
    :return:
    '''
    pass


def on_message(client, userdata, message):
    '''
    当收到关于客户端订阅的主题消息时调用
    :param client:
    :param userdata:
    :param msg: 描述所有消息参数的 mqtt message
    :return:
    '''
    print(message.topic + "" + str(message.payload))


def on_publish(client, userdata, mid):
    '''
    当使用client.publish() 发送的消息已经传输到代理时被调用
    对于qos级别 1和2的消息  调用时 意味着已经完成和代理的握手
    对于qos级别为0的消息,   调用时 只意味着消息离开了客户端
    :param client:
    :param userdata:
    :param mid:  这个变量与client.publish() 返回的mid变量匹配  用来跟踪传出的消息
    :return:
    '''
    pass


def on_subscribe(client, userdata, mid, granted_qos):
    '''
    当代理响应订阅请求时被调用
    :param client:
    :param userdata:
    :param mid: 变量与 client.subscribe() 返回的mid变量匹配
    :param granted_qos: 是一个整数列表  提供了代理为每个不同的订阅请求授予的qos级别
    :return:
    '''


def on_unsubscribe(client, userdata, mid):
    '''
    当代理响应取消订阅请求时调用
    :param client:
    :param userdata:
    :param mid: 变量匹配 client.unsubscribe()返回的mid变量
    :return:
    '''


def on_log(client, userdata, level, buf):
    '''
    当客户端有日志信息时调用
    :param client:
    :param userdata:
    :param level:消息的严重性，是MQTT_LOG_INFO，MQTT_LOG_NOTICE，MQTT_LOG_WARNING，MQTT_LOG_ERR和MQTT_LOG_DEBUG中的一个。
    :param buf: 存储的信息
    :return:
    '''


# 函数

# 构造client  构造函数Client()
# client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
# client_id 连接到代理时使用的唯一客户端ID字符串。 如果client_id长度为零或无，则会随机生成一个。 在这种情况下，clean_session参数必须为True。
# clean_session 一个决定客户端类型的布尔值 在django服务中的客户端可以设置为false。  如果为True，那么代理将在其断开连接时删除有关此客户端的所有信息。 如果为False，则客户端是持久客户端，当客户端断开连接时，订阅信息和排队消息将被保留。
# userdata 用户定义的任何类型的数据作为userdata参数传递给回调函数。 它可能会在稍后使用client.user_data_set（）函数进行更新。
# protocol  用于此客户端的MQTT协议的版本。 可以是MQTTv31或MQTTv311。 一般不用写 用默认的即可
# transport 设置为“websockets”通过WebSockets发送MQTT。 默认的“tcp”使用原始TCP。
import paho.mqtt.client as mqtt

client = mqtt.Client()

# 将客户端重置为开始状态,即恢复到创建状态  采用和Client()构造函数相同的参数
client.reinitialise()

# 选项函数
# 设置QoS> 0的消息的最大数量，消息一次通过网络流量的最大数量。默认为20.增加此值将消耗更多内存，但可以增加吞吐量。
client.max_inflight_messages_set(20)

# 设置传出消息队列中可等待处理的具有QoS> 0的传出消息的最大数量。默认为0表示无限制。 当队列已满时，任何其他传出的消息都将被丢弃。
client.max_queued_messages_set(0)

# 如果代理没有响应，设置在重发QoS> 0的消息之前以秒为单位的时间。默认设置为5秒，通常不需要更改。
client.message_retry_set(5)

# 设置websocket连接选项。 只有在transport =“websockets”被传入Client（）构造函数时才会使用这个选项。
# path 代理使用的mqtt路径   header 可以是一个字典，指定应该附加到标准websocket头部的额外头部列表，也可以是可调用的正常websocket头部并返回带有一组头部以连接到代理的新字典。
client.ws_set_options(path="/mqtt", headers=None)

# 配置网络加密和身份验证选项。 启用SSL / TLS支持。
#  ca_certs  证书颁发机构证书文件的字符串路径
# certfile, keyfile  分别指向PEM编码的客户端证书和私钥的字符串。 如果这些参数不是None，那么它们将用作基于TLS的身份验证的客户端信息。 对此功能的支持取决于代理。
# cert_reqs 定义客户对经纪人施加的证书要求。 默认情况下，这是ssl.CERT_REQUIRED，这意味着代理必须提供证书。 有关此参数的更多信息，请参阅ssl pydoc。
# tls_version  指定要使用的SSL / TLS协议的版本。 默认情况下（如果python版本支持它），检测到最高的TLS版本。
# ciphers  指定哪些加密密码可供此连接使用的字符串，或者使用None来使用默认值。 有关更多信息，请参阅ssl pydoc。
# client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
#                tls_version=ssl.PROTOCOL_TLS, ciphers=None)

# 配置服务器证书中服务器主机名的验证。
# 如果value设置为True，则不可能保证您连接的主机不模拟您的服务器。 这在初始服务器测试中可能很有用，但是，恶意的第三方通过可以DNS欺骗模拟您的服务器。
# client.tls_insecure_set(value=False)

# 使用标准的Python日志包启用日志记录。 这可以与on_log回调方法同时使用
# 如果指定了记录器，那么将使用该logging.Logger对象，否则将自动创建一个。
client.enable_logger()

# 使用标准python日志包禁用日志记录。 这对on_log回调没有影响。
client.disable_logger()

# 为客户端的代理认证设置用户名和 密码(密码可不写)
client.username_pw_set("admin", "password")

# 设置在生成事件时将传递给回调的私人用户数据。 可以自己定义一些信息
client.user_data_set('userdata')

# 设置要发送给代理的遗嘱   客户端断开而没有调用disconnect(), 代理将代表客户端发布消息
# topic 是 消息发布的主题   payload 是 发布的消息  qos 是遗嘱的质量等级  retain 如果为True 遗嘱消息将被设置为该主题的“最后已知良好”/保留消息。
client.will_set(topic='yiyan', payload=None, qos=0, retain=False)

# 客户端自动重连   当连接丢失时，最初重新连接尝试延迟min_delay秒。 延迟在随后的尝试到中增加一倍。当连接完成时（例如收到CONNACK，而不仅仅是TCP连接建立），延迟重置为min_delay。
client.reconnect_delay_set(min_delay=1, max_delay=120)

client.on_connect = on_connect
client.on_message = on_message

Host = '127.0.0.1'

# connect() 函数将客户端连接到代理,是一个阻塞函数
# host 代理的主机名 或者 ip地址  port 服务器主机的网络端口
# keepalive 心跳信息发送的速率 如果没有其他消息正在交换，则它将控制客户端向代理发送ping消息的速率
# bind_address
client.connect(host=Host, port=1883, keepalive=60, bind_address="")

# 与loop_start（）一起使用以非阻塞方式连接。 直到调用loop_start（）,连接才会完成。
client.connect_async(host=Host, port=1883, keepalive=60, bind_address="")

# 使用SRV DNS查找连接到代理以获取代理地址。
client.connect_srv()

# 以之前connect()的信息重连代理
client.reconnect()

# 与代理断开连接   不会发送遗嘱消息
client.disconnect()

# 定期调用处理网络事件
# 此调用在select（）中等待，直到网络套接字可用于读取或写入（如果适用），然后处理传入/传出数据。
# 一般写在循环里  直到网络套接字可用于读取 或 写入  然后处理 传入/ 传出数据
client.loop(timeout=1.0, max_packets=1)

#  实现网络循环的线程接口
client.loop_start()
client.loop_stop(force=False)

# 这是网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)

# 从客户端向代理发送消息
# topic是主题  payload 是发送的消息  qos是消息质量级别   retain 如果是true 则该消息是该主题最后已知良好的保留消息
# 如果要传二进制数据  可以用 python 的 strut 模块打包要传的数据
info = client.publish(topic="task", payload="", qos=0, retain=False)
# 返回的以下属性和方法
# rc 发布的结果  mid是 发布的消息id
print(info.rc, info.mid)
# 这个方法 会阻塞,直到消息发布  如果消息未排队 (rc == MQTT_ERR_QUEUE_SIZE) 将引发ValueError
info.wait_for_publish()
# 如果消息已发布，is_published返回True。 如果消息未排队（rc == MQTT_ERR_QUEUE_SIZE），它将引发ValueError
info.is_published()

# 订阅一个 或 多个主题
info = client.subscribe(topic="result", qos=0)
# 函数返回 一个元祖 （result，mid）
# 这是 订阅的 元祖 或 列表形式的 写法
client.subscribe(("result", 0))
client.subscribe([("result", 0), ("task", 0)])

# 取消订阅
client.unsubscribe(topic='result')

# 外部事件循环支持 ( 自定义适配自己的应用时可以调用) 当loop 以 线程形式(connect_async,loop_start)启动时  使用不了以下的方法
client.loop_read()  # 当套接字准备好读取时调用
client.loop_write()  # 当套接字准备好写入时调用
client.loop_misc()  # 每隔几秒呼叫一次以处理消息重试和ping。
client.socket()  # 返回客户端中使用的套接字对象，以允许与其他事件循环进行交互。
client.want_write()  # 如果有数据等待写入，则返回true，以允许将客户端与其他事件循环连接。

# 全局辅助函数


# Publish模块
# 一次性发布消息  发完就断开连接
import paho.mqtt.publish as publish
# 一次性发送一条消息
publish.single(topic='task', payload=None, qos=0, retain=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311, transport="tcp")

# 一次性发送多条消息
msgs = [{'topic':"paho/test/multiple", 'payload':"multiple 1"},
    ("paho/test/multiple", "multiple 2", 0, False)]
publish.multiple(msgs, hostname="localhost", port=1883, client_id="", keepalive=60,
    will=None, auth=None, tls=None, protocol=mqtt.MQTTv311, transport="tcp")


# Subscribe 模块
# 该模块 允许直接订阅和处理消息
import paho.mqtt.subscribe as subscribe

# 订阅一组主题并返回收到的消息,是一个阻塞函数
subscribe.simple(topics='task', qos=0, msg_count=1, retained=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311)

# 订阅一组主题 并 使用自定义的回调函数处理收到的消息
def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

subscribe.callback(callback=on_message_print, topics="result", qos=0, userdata=None, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311)
