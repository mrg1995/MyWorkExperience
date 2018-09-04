# Sessions

channels 支持 django的session在HTTP和Websocket中使用http cookie

### 基本用法

在channels中支持django session的中间键是 `SessionMiddleware` ,但是它需要 `CookieMiddleware` ,在channels中 `SessionMiddlewareStack` 包含了以上两个中间件

使用中间键示例:

```python
# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from myapp import consumers

application = ProtocolTypeRouter({

    "websocket": SessionMiddlewareStack(
        URLRouter([
            url(r"^front(end)/$", consumers.AsyncChatConsumer),
        ])
    ),

})
```

在使用时 可以用  `self.scope["session"]`  在你的消费者类的代码里

```python
class ChatConsumer(WebsocketConsumer):
    def connect(self, event):
        self.scope["session"]["seed"] = random.randint(1, 1000)
```

### Session Persistence (会话持久性)

在http中session是默认自动保存的.

在websocket的消费者中,session不会自动保存,需要手动保存,保存函数为 `scope["session"].save()` ,如果不保存,session还是会照常运行,但是其他连接或视图无法看到session的变化.











