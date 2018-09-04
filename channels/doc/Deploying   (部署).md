# Deploying   (部署)

部署channels 2 (ASGI) 的方式类似于WSGI应用,可以自定义进程数量



### Configuring the ASGI application (配置asgi应用)

在settings.py中写入

```python
ASGI_APPLICATION = "myproject.routing.application"
```

### Setting up a channel backend(配置channel 载体)

```python
#settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-server-name", 6379)],
        },
    },
}
```

这个需要安装 channels_redis.  

channel_redis在安装过程中会出现 一些ms c++ 库的required 报错  ,可以下载安装  

[下载链接]: https://pan.baidu.com/s/1tTEStvJ6-4hVy3cAsOaSIg	"下载链接"

### Run protocol servers  (运行协议服务器)

新建asgi.py文件 

```python
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()
application = get_default_application()
```

运行:

```python
daphne myproject.asgi:application
```

```python
daphne -b 0.0.0.0 -p 8001 myproject.asgi:application
```













