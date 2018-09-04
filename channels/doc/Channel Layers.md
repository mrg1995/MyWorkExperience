# Channel Layers

通道层允许两个不同的通道实例进行对话,可以不通过数据库来进行分布式的实时对话.

通道的载体一般是redis,官方有维护`channels_redis`



### Configuration (配置)

```python
#settings
# 选择通道载体
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-server-name", 6379)],
        },
    },
}
```

可以使用 `channels.layers.get_channel_layer()` 获取到默认的 channel layer ,但在消费中类中,可以使用`self.channel_layer`  来获取

### Synchronous Functions  (同步功能)

channel_layer 的  `send()`, `group_send()`, `group_add()` 都是异步执行的,如果要同步执行的话

例子:

```python
from asgiref.sync import async_to_sync

async_to_sync(channel_layer.send)("channel_name", {...})
```

### What To Send Over The Channel Layer  (发送数据)

示例:

```python
# 广播
# 向通道组里的所有客户端进行广播
await self.channel_layer.group_send(
    room.group_name,  # 通道组名   
    {
        "type": "chat_message",  # 方法名称,调用下面的方法
        "room_id": room_id,
        "username": self.scope["user"].username,
        "message": message,
    }
)

async def chat_message(self, event):
    """
    Called when someone has messaged our chat.
    """
    # Send a message down to the client
    await self.send_json(
        {
            "msg_type": settings.MSG_TYPE_MESSAGE,
            "room": event["room_id"],
            "username": event["username"],
            "message": event["message"],
        },
    )
```

消费者类中一般会自动生成`self.channel_layer` and `self.channel_name` attribute,

### Single Channels  (单通道)

将单通道的通道名写入数据库 例子:

```python
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # 写入数据库
        Clients.objects.create(channel_name=self.channel_name)

    def disconnect(self, close_code):
        # 从数据库中删除
        Clients.objects.filter(channel_name=self.channel_name).delete()
        
	def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
             {
                 'type': 'chat_message',
                 'message': message
             }
         )
    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=json.dumps("message":event["message"]))
```

### Groups

通道组 ,包含许多连接通道,我们可以通过通道名称(`self.channel_name` )向通道组中增加,或者删除连接通道.但是通道不允许枚举或列出组中的通道;这是一个纯粹的广播系统。如果您需要更精确的控制或需要知道连接的是谁，需要构建自己的系统或使用合适的第三方系统。

广播示例:

```python
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # 连接时 将该连接通道加入 chat 组
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)

    def disconnect(self, close_code):
        # 断开连接时  将该连接通道 从chat组里删除
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        
    def receive(self, text_data):
        # 通道接受到 text 时 将信息广播给所有chat组里的client连接
        async_to_sync(self.channel_layer.group_send)(
            "chat",
            {
                "type": "chat_message",
                "text": text_data,
            },
        )

    def chat_message(self, event):
        self.send(text_data=event["text"])
```

### Using Outside Of Consumers (在消费者之外使用通道层)



```python
from channels.layers import get_channel_layer
# 可以通过get_channel_layer() 获取通道层
channel_layer = get_channel_layer()
```

一般通道层的方法都是异步的  因此需要await

```python

for chat_name in chats:
    await channel_layer.group_send(
        chat_name,
        {"type": "chat.system_message", "text": announcement_text},
    )
```

也可以把方法转化为同步执行

```python
from asgiref.sync import async_to_sync

async_to_sync(channel_layer.group_send)("chat", {"type": "chat.force_disconnect"})
```









