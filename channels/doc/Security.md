# Security



### WebSockets

防止csrf (跨站请求伪造) 可以使用 `channels.security.websocket`  中的  `OriginValidator` 和`AllowedHostsOriginValidator`. 

OriginValidator 示例:

```python
from channels.security.websocket import OriginValidator

application = ProtocolTypeRouter({

    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                ...
            ])
        ),
        # 需要些个域名列表
        [".goodsite.com", "http://.goodsite.com:80", "http://other.site.com"],
    ),
})
```

AllowedHostsOriginValidator 示例:

```python
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({

    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                ...
            ])
        ),
    ),
})
```

AllowedHostsOriginValidator  直接会自动加载django  setting中的 ALLOWED_HOSTS 列表.









