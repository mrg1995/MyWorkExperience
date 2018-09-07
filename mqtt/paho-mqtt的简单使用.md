# 一、Client模块

与MQTT代理（broker）进行通信的主要类。

------

## （一）使用流程

- 使用`connect()`/`connect_async()` 连接MQTT代理

- 频繁的调用

  ```
  loop()
  ```

  来维持与MQTT代理之间的流量

   

  ​

  - 或者使用`loop_start()`来设置一个线程为你调用`loop()`
  - 或者在一个阻塞的函数中调用`loop_forever()`来为你调用`loop()`

- 使用`subscribe()`订阅一个主题（topic）并接受消息（messages）

- 使用`publish()`来发送消息

- 使用`disconnect()`来断开与MQTT代理的连接

------

## （二）回调(Callbacks)

### 1.基本概念

使用回调处理从MQTT代理返回的数据，要使用回调需要先定义回调函数然后将其指派给客户端实例（client）。 
例如：

```
# 定义一个回调函数
def on_connect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))

# 将回调函数指派给客户端实例
client.on_connect = on_connect
```

所有的回调函数都有`client`和`userdata`参数。 
`client`是调用回调的客户端实例； 
`userdata`可以使任何类型的用户数据，可以在创建新客户端实例时设置或者使用user_data_set(userdata)设置。

### 2.回调种类

#### （1）on_connect()

当代理响应连接请求时调用。 
`on_connect(client, userdata, flags, rc):` 
`flags`是一个包含代理回复的标志的字典； 
`rc`的值决定了连接成功或者不成功：

| 值    | 连接情况      |
| ---- | --------- |
| 0    | 连接成功      |
| 1    | 协议版本错误    |
| 2    | 无效的客户端标识  |
| 3    | 服务器无法使用   |
| 4    | 错误的用户名或密码 |
| 5    | 未经授权      |

#### （2）on_disconnect()

当与代理断开连接时调用

```
on_disconnect(client, userdata, rc):1
```

`rc`参数表示断开状态。 
如果MQTT_ERR_SUCCESS（0），回调被调用以响应disconnect（）调用。 如果以任何其他值断开连接是意外的，例如可能出现网络错误。

#### （3）on_message()

```
on_message(client, userdata, message):1
```

当收到关于客户订阅的主题的消息时调用。 
`message`是一个描述所有消息参数的MQTTMessage。

#### （4）on_publish()

当使用使用`publish()`发送的消息已经传输到代理时被调用。

```
on_publish(client, userdata, mid):1
```

对于Qos级别为1和2的消息，这意味着已经完成了与代理的握手。 
对于Qos级别为0的消息，这只意味着消息离开了客户端。 
`mid`变量与从相应的`publish()`返回的mid变量匹配，以允许跟踪传出的消息。

> 此回调很重要，因为即使publish（）调用返回，但并不总意味着消息已发送。

#### （5）on_subscribe()

当代理响应订阅请求时被调用。

```
on_subscribe(client, userdata, mid, granted_qos):1
```

`mid`变量匹配从相应的`subscri be()`返回的`mid`变量。 
‘granted_qos’变量是一个整数列表，它提供了代理为每个不同的订阅请求授予的QoS级别。

#### （6）on_unsubscribe()

当代理响应取消订阅请求时调用。

```
on_unsubscribe(client, userdata, mid):1
```

`mid`匹配从相应的unsubscribe（）调用返回的中间变量。

#### （7）on_log()

当客户端有日志信息时调用

```
on_log(client, userdata, level, buf):1
```

`level`变量给出了消息的严重性，并且将是MQTT_LOG_INFO，MQTT_LOG_NOTICE，MQTT_LOG_WARNING，MQTT_LOG_ERR和MQTT_LOG_DEBUG中的一个。 
`buf`变量用于存储信息。

------

## （三）方法

### 1.构造函数Client（）

```
Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")1
```

| 参数            | 含义                                       |
| ------------- | ---------------------------------------- |
| client_id     | 连接到代理时使用的唯一客户端ID字符串。 如果client_id长度为零或无，则会随机生成一个。 在这种情况下，clean_session参数必须为True。 |
| clean_session | 一个决定客户端类型的布尔值。 如果为True，那么代理将在其断开连接时删除有关此客户端的所有信息。 如果为False，则客户端是持久客户端，当客户端断开连接时，订阅信息和排队消息将被保留。 |
| userdata      | 用户定义的任何类型的数据作为userdata参数传递给回调函数。 它可能会在稍后使用user_data_set（）函数进行更新。 |
| protocol      | 用于此客户端的MQTT协议的版本。 可以是MQTTv31或MQTTv311。   |
| transport     | 设置为“websockets”通过WebSockets发送MQTT。 保留默认的“tcp”使用原始TCP。 |

示例：

```
import paho.mqtt.client as mqtt
client = mqtt.Client()12
```

### 2.reinitialise()

```
reinitialise(client_id="", clean_session=True, userdata=None)1
```

reinitialise（）函数将客户端重置为其开始状态，就像它刚刚创建一样。 它采用与Client（）构造函数相同的参数。 
示例：

```
client.reinitialise()1
```

### 3.选项函数

这些函数表示可以在客户端上设置以修改其行为的选项。 在大多数情况下，这必须在连接到代理之前完成。

#### （1）max_inflight_messages_set()

```
max_inflight_messages_set(self, inflight)1
```

设置QoS> 0的消息的最大数量，该消息一次可以部分通过其网络流量。默认为20.增加此值将消耗更多内存，但可以增加吞吐量。

#### （2）max_queued_messages_set()

```
max_queued_messages_set(self, queue_size)1
```

设置传出消息队列中可等待处理的具有QoS> 0的传出消息的最大数量。默认为0表示无限制。 当队列已满时，任何其他传出的消息都将被丢弃。

#### （3）message_retry_set（）

```
message_retry_set(retry)1
```

如果代理没有响应，设置在重发QoS> 0的消息之前以秒为单位的时间。默认设置为5秒，通常不需要更改。

#### （4）ws_set_options()

```
ws_set_options(self, path="/mqtt", headers=None)1
```

设置websocket连接选项。 只有在transport =“websockets”被传入Client（）构造函数时才会使用这些选项。

| 参数      | 含义                                       |
| ------- | ---------------------------------------- |
| path    | 代理使用的mqtt路径                              |
| headers | 可以是一个字典，指定应该附加到标准websocket头部的额外头部列表，也可以是可调用的正常websocket头部并返回带有一组头部以连接到代理的新字典。 |

> 必须在调用connect()之前调用。

#### （4）tls_set()

```
tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)12
```

配置网络加密和身份验证选项。 启用SSL / TLS支持。

| 参数                | 含义                                       |
| ----------------- | ---------------------------------------- |
| ca_certs          | 证书颁发机构证书文件的字符串路径，该证书文件将被视为受此客户端信任。       |
| certfile, keyfile | 分别指向PEM编码的客户端证书和私钥的字符串。 如果这些参数不是None，那么它们将用作基于TLS的身份验证的客户端信息。 对此功能的支持取决于代理。 |
| cert_reqs         | 定义客户对经纪人施加的证书要求。 默认情况下，这是ssl.CERT_REQUIRED，这意味着代理必须提供证书。 有关此参数的更多信息，请参阅ssl pydoc。 |
| tls_version       | 指定要使用的SSL / TLS协议的版本。 默认情况下（如果python版本支持它），检测到最高的TLS版本。 |
| ciphers           | 指定哪些加密密码可供此连接使用的字符串，或者使用None来使用默认值。 有关更多信息，请参阅ssl pydoc。 |

> 必须在调用connect()之前调用。

#### （5）tls_set_context()

配置网络加密和认证上下文。 启用SSL / TLS支持。

```
tls_set_context(context=None)1
```

| 参数      | 含义                  |
| ------- | ------------------- |
| context | 一个ssl.SSLContext对象。 |

> 必须在调用connect()之前调用。

#### （6）tls_insecure_set()

配置服务器证书中服务器主机名的验证。

```
tls_insecure_set(value)1
```

如果value设置为True，则不可能保证您连接的主机不模拟您的服务器。 这在初始服务器测试中可能很有用，但是，恶意的第三方通过可以DNS欺骗模拟您的服务器。

> - 请勿在真实系统中使用此功能。 将值设置为True意味着使用加密没有意义。
> - 必须在connect*（）之前和tls_set（）或tls_set_context（）之后调用。

#### （7）enable_logger()

使用标准的Python日志包启用日志记录。 这可以与on_log回调方法同时使用

```
enable_logger(logger=None)1
```

如果指定了记录器，那么将使用该logging.Logger对象，否则将自动创建一个。 
按照以下映射将Paho日志记录级别转换为标准日志级别：

| Paho             | logging                             |
| ---------------- | ----------------------------------- |
| MQTT_LOG_ERR     | ligging.ERROR                       |
| MQTT_LOG_WARNING | logging.WARNING                     |
| MQTT_LOG_NOTICE  | logging.INFO (no direct equivalent) |
| MQTT_LOG_INFO    | logging.INFO                        |
| MQTT_LOG_DEBUG   | logging.DEBUG                       |

#### （8）disable_logger()

使用标准python日志包禁用日志记录。 这对on_log回调没有影响。

```
disable_logger()1
```

#### （9）username_pw_set()

为代理认证设置一个用户名和一个可选的密码。必须在connect*（）之前调用。

```
username_pw_set(username, password=None)1
```

#### （10）user_data_set()

设置在生成事件时将传递给回调的私人用户数据。 将其用于您自己的目的以支持您的应用程序。

```
user_data_set(userdata)1
```

#### （11）will_set()

设置要发送给代理的遗嘱。 如果客户端断开而没有调用disconnect（），代理将代表它发布消息。

```
will_set(topic, payload=None, qos=0, retain=False)1
```

| 参数      | 含义                                    |
| ------- | ------------------------------------- |
| topic   | 该遗嘱消息发布的主题                            |
| payload | 该消息将作为遗嘱发送                            |
| qos     | 用于遗嘱的服务质量等级                           |
| retain  | 如果设置为True，遗嘱消息将被设置为该主题的“最后已知良好”/保留消息。 |

> 如果qos不是0,1或2，或者主题为None或字符串长度为零，则引发ValueError。

#### （11）reconnect_delay_set（）

客户端将自动重试连接。 在每次尝试之间，它会在min_delay和max_delay之间等待几秒钟。

```
reconnect_delay_set(min_delay=1, max_delay=120)1
```

当连接丢失时，最初重新连接尝试延迟min_delay秒。 延迟在随后的尝试到中增加一倍。当连接完成时（例如收到CONNACK，而不仅仅是TCP连接建立），延迟重置为min_delay。

### 4.connect()

connect（）函数将客户端连接到代理。 这是一个阻塞函数。

```
connect(host, port=1883, keepalive=60, bind_address="")1
```

| 参数           | 含义                                       |
| ------------ | ---------------------------------------- |
| host         | 远程代理的主机名或IP地址                            |
| port         | 要连接的服务器主机的网络端口。 默认为1883                  |
| keepalive    | 与代理通信之间允许的最长时间段（以秒为单位）。 如果没有其他消息正在交换，则它将控制客户端向代理发送ping消息的速率 |
| bind_address | 假设存在多个接口，将绑定此客户端的本地网络接口的IP地址             |

### 5.connect_async()

与loop_start（）一起使用以非阻塞方式连接。 直到调用loop_start（）之前，连接才会完成。

```
connect_async(host, port=1883, keepalive=60, bind_address="")1
```

### 6.connect_srv()

使用SRV DNS查找连接到代理以获取代理地址。

```
connect_srv(domain, keepalive=60, bind_address="")1
```

| 参数     | 含义                           |
| ------ | ---------------------------- |
| domain | 该DNS域搜索SRV记录。 如果无，请尝试确定本地域名。 |

### 7.reconnect()

使用先前提供的详细信息重新连接到经纪商。 在调用此函数之前，您必须先调用connect *（）。

```
reconnect()1
```

### 8.disconnect()

干净地从代理断开连接。 使用disconnect（）不会导致代理发送遗嘱消息。

```
disconnect()1
```

### 9.loop()

定期调用处理网络事件。

```
loop(timeout=1.0, max_packets=1)1
```

此调用在select（）中等待，直到网络套接字可用于读取或写入（如果适用），然后处理传入/传出数据。

| 参数          | 含义                          |
| ----------- | --------------------------- |
| timeout     | 此方法最多可阻塞timeout秒            |
| max_packets | max_packets参数已过时，应保留为未设置状态。 |

示例：

```
run = True
while run:
    client.loop()123
```

### 10.loop_start() / loop_stop()

这些功能实现了到网络循环的线程接口。

```
loop_start()
loop_stop(force=False)12
```

在connect*（）之前或之后调用loop_start（）一次，会在后台运行一个线程来自动调用loop（）。这释放了可能阻塞的其他工作的主线程。这个调用也处理重新连接到代理。 
调用loop_stop（）来停止后台线程。

> force参数目前被忽略。 
> 示例：

```
client.connect("iot.eclipse.org")
client.loop_start()

while True:
    temperature = sensor.blocking_read()
    client.publish("paho/temperature", temperature)123456
```

### 11.loop_forever()

这是网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。

```
loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)1
```

除了使用connect_async时的第一次连接尝试以外，请使用retry_first_connection = True使其重试第一个连接。**这可能会导致客户端连接到一个不存在的主机的情况**。

### 12.publish()

从客户端发送消息给代理。

```
publish(topic, payload=None, qos=0, retain=False)1
```

消息将会发送给代理，并随后从代理发送到订阅匹配主题的任何客户端。

| 参数      | 含义                                       |
| ------- | ---------------------------------------- |
| topic   | 该消息发布的主题                                 |
| payload | 要发送的实际消息。如果没有给出，或设置为无，则将使用零长度消息。 传递int或float将导致有效负载转换为表示该数字的字符串。 如果你想发送一个真正的int / float，使用struct.pack（）来创建你需要的负载 |
| qos     | 服务的质量级别                                  |
| retain  | 如果设置为True，则该消息将被设置为该主题的“最后已知良好”/保留的消息    |

返回以下属性和方法的MQTTMessageInfo: 
**rc**:发布的结果。

| 内容                  | 含义                                       |
| ------------------- | ---------------------------------------- |
| MQTT_ERR_SUCCESS    | 成功                                       |
| MQTT_ERR_NO_CONN    | 客户端当前未连接                                 |
| MQTT_ERR_QUEUE_SIZE | 当使用max_queued_messages_set来指示消息既不排队也不发送。 |

**mid**:发布请求的消息ID。 
如果mid已定义，则可以通过检查on_publish（）回调中的mid来跟踪发布请求。 
**wait_for_publish()**:函数将阻塞，直到消息发布。 如果消息未排队（rc == MQTT_ERR_QUEUE_SIZE），它将引发ValueError。 
**is_published**:如果消息已发布，is_published返回True。 如果消息未排队（rc == MQTT_ERR_QUEUE_SIZE），它将引发ValueError。

> 如果主题为无，长度为零或无效（包含通配符），qos不是0,1或2之一，或者有效负载长度大于268435455字节，则会引发ValueError。

### 13.subscribe()

```
subscribe(topic, qos=0)1
```

订阅一个或多个主题。 
这个函数可以用三种不同的方式调用：

#### （1）简单的字符串和整数

```
subscribe("my/topic", 2)1
```

| 参数    | 值                |
| ----- | ---------------- |
| topic | 一个字符串，指定要订阅的订阅主题 |
| qos   | 期望的服务质量等级。 默认为0。 |

#### （2）字符串和整数元组

```
subscribe(("my/topic", 1))1
```

| 参数    | 值                                |
| ----- | -------------------------------- |
| topic | （topic，qos）的元组。 主题和qos都必须存在于元组中。 |
| qos   | 没有使用                             |

#### （3）字符串和整数元组的列表

这允许在单个SUBSCRIPTION命令中使用多个主题订阅，这比使用多个订阅subscribe（）更有效。

```
subscribe([("my/topic", 0), ("another/topic", 2)])1
```

| 参数    | 值                                        |
| ----- | ---------------------------------------- |
| topic | 格式元组列表（topic，qos）。 topic和qos都必须出现在所有的元组中。 |
| qos   | 没有使用                                     |

该函数返回一个元组（result，mid）。

> 如果qos不是0,1或2，或者主题为None或字符串长度为零，或者topic不是字符串，元组或列表，则引发ValueError。

### 14.unsubscribe()

取消订阅一个或多个主题。

```
unsubscribe(topic)1
```

| 参数    | 含义              |
| ----- | --------------- |
| topic | 主题的单个字符串或者字符串列表 |

返回一个元组(result, mid)

### 15.外部事件循环支持

#### （1）loop_read()

```
loop_read(max_packets=1)1
```

当套接字准备好读取时调用。 max_packets已过时，应保持未设置状态。

#### （2）loop_write()

```
loop_write(max_packets=1)1
```

当套接字准备好写入时调用。 max_packets已过时，应保持未设置状态。

#### （3）loop_misc()

```
loop_misc()1
```

每隔几秒呼叫一次以处理消息重试和ping。

#### （4）socket()

```
socket()1
```

返回客户端中使用的套接字对象，以允许与其他事件循环进行交互。

#### （5）want_write()

```
want_write()1
```

如果有数据等待写入，则返回true，以允许将客户端与其他事件循环连接。

### 16.全局辅助函数

client模块还提供了一些全局帮助函数。 
(1)`topic_matches_sub（sub，topic）`可用于检查主题是否与预订匹配。 
(2)`connack_string（connack_code）`返回与CONNACK结果关联的错误字符串。 
(3)`error_string（mqtt_errno）`返回与Paho MQTT错误号关联的错误字符串。

------

# 二、Publish模块

该模块提供了一些帮助功能，可以以一次性方式直接发布消息。换句话说，它们对于您想要发布给代理的单个/多个消息然后断开与其他任何必需的连接的情况非常有用。

## （一）方法

### 1.Single

将一条消息发布给代理，然后彻底断开连接。

```
single(topic, payload=None, qos=0, retain=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311, transport="tcp")123
```

| 参数        | 含义                                       |
| --------- | ---------------------------------------- |
| topic     | 唯一必需的参数必须是负载将发布到的主题字符串。                  |
| payload   | 要发布的有效载荷。 如果“”或None，零长度的有效载荷将被发布         |
| qos       | 发布时使用的qos默认为0                            |
| retain    | 设置消息保留（True）或不（False）                    |
| hostname  | 一个包含要连接的代理地址的字符串。 默认为localhost           |
| port      | 要连接到代理的端口。 默认为1883                       |
| client_id | 要使用的MQTT客户端ID。 如果“”或None，Paho库会自动生成客户端ID |
| keepalive | 客户端的存活超时值。 默认为60秒                        |
| will      | 一个包含客户端遗嘱参数的字典,`will = {‘topic’: “<topic>”, ‘payload’:”<payload”>, ‘qos’:<qos>, ‘retain’:<retain>}.` |
| auth      | 一个包含客户端验证参数的字典,`auth = {‘username’:”<username>”, ‘password’:”<password>”}` |
| tls       | 一个包含客户端的TLS配置参数的字典,`dict = {‘ca_certs’:”<ca_certs>”, ‘certfile’:”<certfile>”, ‘keyfile’:”<keyfile>”, ‘tls_version’:”<tls_version>”, ‘ciphers’:”<ciphers”>}` |
| protocol  | 选择要使用的MQTT协议的版本。 使用MQTTv31或MQTTv311。     |
| transport | 设置为“websockets”通过WebSockets发送MQTT。 保留默认的“tcp”使用原始TCP。 |

示例：

```
import paho.mqtt.publish as publish

publish.single("paho/test/single", "payload", hostname="iot.eclipse.org")123
```

### 2.Multiple

将多条消息发布给代理，然后干净地断开连接。

```
multiple(msgs, hostname="localhost", port=1883, client_id="", keepalive=60,
    will=None, auth=None, tls=None, protocol=mqtt.MQTTv311, transport="tcp")12
```

| 参数   | 含义                                       |
| ---- | ---------------------------------------- |
| msgs | 要发布的消息列表。 每条消息是一个字典或一个元组。`msg = {‘topic’:”<topic>”, ‘payload’:”<payload>”, ‘qos’:<qos>, ‘retain’:<retain>}`或`(“<topic>”, “<payload>”, qos, retain)` |

> 有关hostname，port，client_id，keepalive，will，auth，tls，protocol，transport的描述，请参阅single（）。 
> 示例：

```
import paho.mqtt.publish as publish

msgs = [{'topic':"paho/test/multiple", 'payload':"multiple 1"},
    ("paho/test/multiple", "multiple 2", 0, False)]
publish.multiple(msgs, hostname="iot.eclipse.org")12345
```

------

# 三、Subscribe模块

该模块提供了一些帮助功能，以允许直接订阅和处理消息。

## （1）方法

### 1.Simple

订阅一组主题并返回收到的消息。 这是一个阻塞函数。

```
simple(topics, qos=0, msg_count=1, retained=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311)123
```

| 参数        | 含义                                       |
| --------- | ---------------------------------------- |
| topics    | 唯一需要的参数是客户端将订阅的主题字符串。 如果需要订阅多个主题，这可以是字符串或字符串列表 |
| qos       | 订阅时使用的qos默认为0                            |
| msg_count | 从代理检索的消息数量。 默认为1.如果为1，则返回一个MQTTMessage对象。 如果> 1，则返回MQTTMessages列表 |
| retained  | 设置为True以考虑保留的消息，将其设置为False以忽略具有保留标志设置的消息 |
| hostname  | 一个包含要连接的代理地址的字符串。 默认为localhost           |
| port      | 要连接到代理的端口。 默认为1883                       |
| client_id | 要使用的MQTT客户端ID。 如果“”或None，Paho库会自动生成客户端ID |
| keepalive | 客户端的存活超时值。 默认为60秒。                       |
| will      | 一个包含客户端遗嘱参数的字典,`will = {‘topic’: “<topic>”, ‘payload’:”<payload”>, ‘qos’:<qos>, ‘retain’:<retain>}.` |
| auth      | 一个包含客户端验证参数的字典,`auth = {‘username’:”<username>”, ‘password’:”<password>”}` |
| tls       | 一个包含客户端的TLS配置参数的字典,`dict = {‘ca_certs’:”<ca_certs>”, ‘certfile’:”<certfile>”, ‘keyfile’:”<keyfile>”, ‘tls_version’:”<tls_version>”, ‘ciphers’:”<ciphers”>}` |
| protocol  | 选择要使用的MQTT协议的版本。 使用MQTTv31或MQTTv311。     |

### 2.Callback

订阅一组主题并使用用户提供的回叫处理收到的消息。

```
callback(callback, topics, qos=0, userdata=None, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311)123
```

| 参数       | 含义                                      |
| -------- | --------------------------------------- |
| callback | 一个“on_message”回调将被用于每个收到的消息             |
| topics   | 客户端将订阅的主题字符串。 如果需要订阅多个主题，这可以是字符串或字符串列表。 |
| qos      | 订阅时使用的qos默认为0                           |
| userdata | 用户提供的对象将在收到消息时传递给on_message回调函数         |

> 有关hostname，port，client_id，keepalive，will，auth，tls，protocol的描述，请参阅simple（）。 
> 示例：

```
import paho.mqtt.subscribe as subscribe

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

subscribe.callback(on_message_print, "paho/test/callback", hostname="iot.eclipse.org"123456
```

------

参考资料：<https://pypi.python.org/pypi/paho-mqtt>