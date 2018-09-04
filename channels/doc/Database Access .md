# Database Access 

django的orm是同步代码,如果要在异步的代码中调用它的话需要特殊处理,来保证与数据库的连接断开.

如果使用的是同步消费者,或者基于同步消费者的通用消费者,就不需要做特殊处理

如果使用的异步代码,为了安全使用数据库方法,使用`database_sync_to_async`

### Database Connections

一般线程数量开的是cpu数量 * 5,但是为了避免浪费资源(没处理时,也开着线程),可以重写代码以使用异步使用者，并且只在需要使用Django的ORM时使用线程(使用`database_sync_to_async`)

### database_sync_to_async

`channels.db.database_sync_to_async` 是`asgiref.sync` 的一个版本。会也在退出时清理数据库连接。

使用例子:

```python
from channels.db import database_sync_to_async

async def connect(self):
    self.username = await database_sync_to_async(self.get_name)()

def get_name(self):
    return User.objects.all()[0].name
```

也可以以装饰器的形式

```python
from channels.db import database_sync_to_async

async def connect(self):
    self.username = await self.get_name()

@database_sync_to_async
def get_name(self):
    return User.objects.all()[0].name
```







