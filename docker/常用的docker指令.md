## 常用的docker指令

### 清理所有处于终止状态的容器

用 `docker container ls -a` 命令可以查看所有已经创建的包括终止状态的容器，如果数量太多要一个个删除可能会很麻烦，用下面的命令可以清理掉所有处于终止状态的容器。

```
$ docker container prune
```

### 进入容器

```
docker exec -it name bash
```

### 构建镜像

这里我们使用了 `docker build` 命令进行镜像构建。其格式为：

```
docker build [选项] <上下文路径/URL/->
docker build -t nginx:11.27 .
```

### 删除虚悬镜像

这类镜像被称为 `dangling` - 虚悬镜像。这些镜像可以删除，手动删除 dangling 镜像：

```
docker image prune
```