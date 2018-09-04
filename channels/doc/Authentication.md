# Authentication

channels支持django的身份认证直接使用在HTTP和websocket的消费者上,也可以自定义认证方式.



### Django authentication

`AuthMiddlewareStack`  包含了`AuthMiddleware` ,`SessionMiddleware` ,`CookieMiddleware`.

使用示例:

```python
# routing.py
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from myapp import consumers

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^front(end)/$", consumers.AsyncChatConsumer),
        ])
    ),
})
```

要访问用户,只要 `self.scope["user"]` 即可

```python
class ChatConsumer(WebsocketConsumer):
    def connect(self, event):
        self.user = self.scope["user"]
```



### Custom Authentication  (自定义的身份验证)

示例 通过用户id来验证:

```python
from django.db import close_old_connections

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)
        user = User.objects.get(id=int(scope["query_string"]))
        # 操作完数据库后,需要关闭连接,这一步目前版本必须得写
        close_old_connections()
        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=user))
```



### How to log a user in/out

channels中有 `channels.auth.login` 和 `channels.auth.logout`. 就和 django中的 `contrib.auth` 中的方法类似

示例:

```python
from channels.auth import login

class ChatConsumer(AsyncWebsocketConsumer):

    ...

    async def receive(self, text_data):
        ...
        # login the user to this session.
        await login(self.scope, user)
        # 登录后session会改变,需要手动保存  
        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        await sync_to_async(self.scope["session"].save)()
```

当在同步函数中使用 `login(scope, user)` , `logout(scope)` or `get_user(scope)` 方法,需要使用 `async_to_sync` 把它们转化为同步

示例:

```python
from asgiref.sync import async_to_sync
from channels.auth import login

class SyncChatConsumer(WebsocketConsumer):

    ...

    def receive(self, text_data):
        ...
        async_to_sync(login)(self.scope, user)
        self.scope["session"].save()
```





































