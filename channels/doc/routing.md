# routing

一般是 `ProtocolTypeRouter` 作为根路由,并在其中嵌入其他协议的路由

看个例子:

```python
from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.consumers import AdminChatConsumer, PublicChatConsumer
from aprs_news.consumers import APRSNewsConsumer

application = ProtocolTypeRouter({
	#http协议会channels会自动写入
    
    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^chat/admin/$", AdminChatConsumer),
            url(r"^chat/$", PublicChatConsumer),
        ])
    ),
	#第三方应用 的 APRS协议
    # Using the third-party project frequensgi, which provides an APRS protocol
    "aprs": APRSNewsConsumer,

})
```

### ProtocolTypeRouter

`channels.routing.ProtocolTypeRouter`

一般作为channels中的顶级路由

```python
ProtocolTypeRouter({
    "http": some_app,
    "websocket": some_other_app,
})
```

http的路由会自动写入,这样就会按照django默认的方式处理请求,如果想要轮询一部分http路由,可以使用URLRouter 和`channels.http.AsgiHandler` 

### URLRouter

`channels.routing.URLRouter`

```python
URLRouter([
    url(r"^longpoll/$", LongPollConsumer),
    url(r"^notifications/(?P<stream>\w+)/$", LongPollConsumer),
    url(r"", AsgiHandler),
])
```

如果要提取上面的stream 参数

```python
stream = self.scope["url_route"]["kwargs"]["stream"]
```



