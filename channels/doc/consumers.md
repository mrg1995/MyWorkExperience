## consumers (消费者)

### 基本消费者

#### AsyncConsumer(异步消费者)

 `channels.consumer.AsyncConsumer`

```python
from channels.consumer import AsyncConsumer

class EchoConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
```

如果要在异步消费者中运行同步函数,可以使用`asgiref.sync.sync_to_async`, 是channels中在线程池中运行同步消费者,可以将任意同步调用转化成异步处理.

#### SyncConsumer(同步消费者)

 `channels.consumer.SyncConsumer`

```python
from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
```

#### Channel Layers (通道层)

一个client(以下均用c表示)通过websocket连接上服务器后,会占用一个通道,消费者类中的函数还可以操作通道层,这样就能使得1对1 ,或者1对多等 进行通信了.

#### scope(域)

类似于http协议中的request

- `scope["path"]`, the path on the request. *(HTTP and WebSocket)*
- `scope["headers"]`, raw name/value header pairs from the request *(HTTP and WebSocket)*
- `scope["method"]`, the method name used for the request. *(HTTP)*

```python
# routing.py
websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

# consumers.py
self.scope['url_route']['kwargs']['room_name'] # 获取url中的参数

```

### 通用消费者

#### WebsocketConsumer  (同步消费者)

只处理和传输text和binary frames

```python
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        # 连接时调用
        # 接受连接:
        self.accept()
        # or选择一个子协议
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        self.accept("subprotocol")
        # or  拒绝连接:
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        # 连接后接收到任意text 或 byte 时调用
        # 你可以发送回去text:
        self.send(text_data="Hello world!")
        # Or, 发送回去二进制数据:
        self.send(bytes_data="Hello world!")
        # 或者断开链接:
        self.close()
        # Or 断开连接 并发送错误码!
        self.close(code=4123)

    def disconnect(self, close_code):
        # 当链接断开时调用
```



#### AsyncWebsocketConsumer(异步消费者)



#### JsonWebsocketConsumer



#### AsyncJsonWebsocketConsumer



#### AsyncHttpConsumer

