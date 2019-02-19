## Docker

### Docker简介
docker 是一种容器技术，作用是用来快速部署服务
Docker 提供了一个开发、打包、运行app的平台

### Docker Engine
- 后台进程 （dockerd）
- REST API server
- CLI接口 （docker）

### 底层技术支持
- Namespaces: 做隔离pid,net,ipc,mnt,uts
- Control groups: 做资源限制
- Union file systems: Container和image的分层

### Image
- 文件和meta data的集合（root filesystem）
- 分层的，并且每一层都可以添加改变删除文件，成为一个新的image
- 不同的image可以共享同样的layer（分层）
- Image本身是read-only

### Image的获取
- Build from Dockerfile
```
FROM ubuntu:14.04          # 基础镜像
LABEL maintainer='natee <nateeinit@xxx.com>' # 构建人信息
RUN apt-get update && apt-get install -y redis-server  # 安装
EXPOSE 6379   # 暴露端口
ENTRYPOINT['/usr/bin/redis-server']
```

- Pull from Registry
```
docker pull ubuntu:14.04
```

### 构建Base Image
- 构建c语言编译环境

> yum install gcc

> yum install glibc-static


- 编写c语言helloworld

> vim hello.c

```c
#include<stdio.h>

int main()
{
    printf("hello natee\n");
}
```

生成可执行文件hello

> gcc -static hello.c -o hello

- 在当前路径编写Dockerfile

> vim Dockerfile

```
FROM scratch  # emtpy image from docker hub
ADD hello /
CMD ['/hello']
```
### Container

- 通过Image创建(copy)
- 在Image layer之上建立一个container layer（可读写）
- 类比面向对象：类和实例
- Image负责app的存储和分发，Container负责运行app

```
   --------------
   |   R/W layer |    ------------>  Container layer
   --------------
      #########   
   ---------------   
  |   9484894e4   |   -------
   ---------------           |---->  Image layers (R/O)
  |   s98232dw3   |   ------- 
   ---------------
```

### 运行Container

- 交互式运行

> docker run -it image-name

但交互式运行后，运行exit会退出运行的docker

- 列出所有container ID

> docker ps -aq

- 清除所有容器

> docker rm $(docker ps -aq)

- 删除已退出的容器

> docker rm $(docker ps -f 'status=exited' -q)

- 通过container创建image

> docker commit container名字 新image名字

- 进入运行的容器
> docker exec -it xxxxxx /bin/bash

- 打开运行的容器的ip
> docker exec -it xxxxx ip a

- 查看容器信息
> docker inspect xxxxxx

- 查看容器运行产生输出log
> docker logs xxxx



### Dockerfile

- FROM
基于哪个Image来制作Image
*尽量使用官方image*

- LABEL
定义Image的Metedata
```
LABEL maintainer='xxx@xxxgmail.com'
LABEL version='1.0'
LABEL descroption='This is description'
```
*LABEL的Metedata不可少*

- RUN （执行命令并创建新的Image Layer）
*每运行一次RUN对于Image都会生成新的一层，对于多命令可以通过 && 组合，复杂的RUN可以 通过 / 换行*

- WOKERDIR
```
WOKREDIR /test # 如果没有会自动创建test目录
WORKDIR demo
RUN pwd  # 输出结果是 /test/demo
```
*使用WORKDIR 不要使用 RUN cd*
*尽量使用绝对目录*

- ADD and COPY
```
ADD test.tar.gz / # 添加到根目录并解压
WORKDIR /root
ADD hello /test # /root/test/hello
```
*大部分情况，copy优先ADD*
*ADD除了COPY还有额外功能（解压）*
*添加远程文件/目录使用curl或者wget*

- ENV
```
ENV MYSQL_VERSION 5.6
RUN apt-get install -y mysql-server= "${MYSQL_VERSION} && rm -rf /var/lib/apt/lists/*"   # 引用常量
```
- VOLUME

- EXPOSE

- CMD （设置容器启动后默认执行的命令和参数）

- ENTRYOPOINT （设置容器启动时运行的命令）
让容器以应用程序或者服务的形式运行
一定不会被忽略，一定会执行


### 打包Python
*准备一段flask-demo*
```python
from flask improt Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'hi natee'
    
if __name__ == '__main__':
    app.run()
```
*编写Dockerfile*
```
FROM python:3.6
LABEL maincontainer= "natee <nateeinit@163.com>"
RUN pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY /root/app.py /app/
WORKDIR /app/
EXPSOE 5000
CMD ["python","app.py"]
```
*生成image*
> build -t natee/flask-demo .


### Docker Network
- 公有IP和私有IP
 - Public IP ： 互联网上的唯一标识，可以访问internet
 - Private IP：不可在互联网上使用，仅供机构内部使用
- 网络地址转换NAT
路由器转换
- Ping和telnet
 - Ping（ICMP）： 验证IP的可达性
 - telnet：验证服务的可用性
- 网络的命名空间
 - 查看：ip netns list
 - 增加： ip netns add test
 
- NameSpace实践

```
# 拉取busybox Image
# 运行两个基于busybox的镜像
# 分别进入两个容器
docker exec -it xxxxxxx /bin/sh
docker exec -it xxxxxx2 /bin/sh
# 查看两个容器的命名空间
ip a
37: eth0@if38: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue 
    link/ether 02:42:ac:12:00:04 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.4/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe12:4/64 scope link 
       valid_lft forever preferred_lft forever
       
ip a
35: eth0@if36: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue 
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe12:3/64 scope link 
       valid_lft forever preferred_lft forever

两个docker中可以互相ping通

```
**network space**
- 查看
> ip netns list

- 创建
> ip netns add test1
> ip netns add test2

- namespace中执行命令
> ip netns exec test1 ip a

```
# 本地回环口
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```
> ip netns exec test1 ip link

```
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```
启动
> ip netns exec test1 ip link set dev lo up

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

- 连接两个namespace（veth pair）
利用Veth

添加一对link
> ip link add veth-test1 type veth peer name veth-test2

查看本地ip link
> ip link

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 00:16:3e:65:15:c3 brd ff:ff:ff:ff:ff:ff
3: br-127caf0addd2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 02:42:c9:2b:eb:6d brd ff:ff:ff:ff:ff:ff
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 02:42:22:25:65:26 brd ff:ff:ff:ff:ff:ff
6: vetheb82e24@if5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-127caf0addd2 state UP mode DEFAULT group default 
    link/ether 9a:dc:fd:23:5a:1b brd ff:ff:ff:ff:ff:ff link-netnsid 0
8: veth24476dd@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-127caf0addd2 state UP mode DEFAULT group default 
    link/ether 32:40:13:30:ff:29 brd ff:ff:ff:ff:ff:ff link-netnsid 2
10: veth33f120f@if9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-127caf0addd2 state UP mode DEFAULT group default 
    link/ether 5a:0c:05:00:3f:59 brd ff:ff:ff:ff:ff:ff link-netnsid 3
12: veth26076b7@if11: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-127caf0addd2 state UP mode DEFAULT group default 
    link/ether d6:0d:16:c9:85:84 brd ff:ff:ff:ff:ff:ff link-netnsid 1
16: veth505d8a5@if15: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default 
    link/ether 66:05:0e:60:63:a6 brd ff:ff:ff:ff:ff:ff link-netnsid 4
36: vethbfcfa02@if35: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default 
    link/ether 3e:b4:db:29:4f:73 brd ff:ff:ff:ff:ff:ff link-netnsid 5
38: veth51eff39@if37: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default 
    link/ether 7a:29:85:0a:c0:2a brd ff:ff:ff:ff:ff:ff link-netnsid 6
39: veth-test2@veth-test1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether a6:68:6d:8a:bf:c8 brd ff:ff:ff:ff:ff:ff
40: veth-test1@veth-test2: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 7e:e4:e4:f7:a6:df brd ff:ff:ff:ff:ff:ff
    
# 多了一对 veth-test1 & veth-test2

```

将veth-test1 添加到test1这个namespace中
> ip link set veth-test1 netns test1

查看test1 namespace
> ip netns exec test1 ip link

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
40: veth-test1@if39: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 7e:e4:e4:f7:a6:df brd ff:ff:ff:ff:ff:ff link-netnsid 0
```
将veth-test2 添加到test2 中，同上
```
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
39: veth-test2@if40: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether a6:68:6d:8a:bf:c8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```
给namespace分配地址
> ip netns exec test1 ip addr add 192.168.1.1/24 dev veth-test1
> ip netns exec test2 ip addr add 192.168.1.2/24 dev veth-test2

启动端口
> ip netns exec test1 ip link set dev veth-test1 up
> ip netns exec test2 ip link set dev veth-test2 up

查看namespace ip 状态

> ip netns exec test1 ip a

```
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
39: veth-test2@if40: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether a6:68:6d:8a:bf:c8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.1.2/24 scope global veth-test2
       valid_lft forever preferred_lft forever
    inet6 fe80::a468:6dff:fe8a:bfc8/64 scope link 
       valid_lft forever preferred_lft forever
```
通过test1 Namespace ping test2
>  ip netns exec test1 ping 192.168.1.2

- 查看docker 网络
> docker network ls

查看network详情
> docker network inspect xxxxx（network id）

```
[
    {
        "Name": "bridge",
        "Id": "48b4577cd31d5da6801288dc0b3e546c11444e30e4045e052a0f2fe6ff11e8cb",
        "Created": "2019-01-23T13:43:52.274217144+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {              
            "1125b71014bfcb4e6e74f48475b40b58bdb3404f4212902b7781460896320876": {
                "Name": "test1",
                "EndpointID": "ed7d3b193f6909a59c50e519a53fdb99eb6135a4aefc3d8074bc6ea84102a150",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```
安装工具包
> yum -y install bridge-untils

查看网桥
brctl show
```
bridge name	bridge id		STP enabled	interfaces
br-127caf0addd2		8000.0242c92beb6d	no		veth24476dd
							veth26076b7
							veth33f120f
							vetheb82e24
docker0		8000.024222256526	no		veth505d8a5
							vethbfcfa02

```
docker网络的连接方式
```

docker1（namespace1) ----(veth)--docker 0（宿主机namespace） --(veth)---docoker2（namespace）
                                  |
                                  |
                                  |
                                 NAT
                                  |
                                  |
                                 外网

```
- Docker Link
创建link 
> docker run -d --name test2 --link test1 busybox /bin/sh -c "while true; do sleep 3600; done"

创建link后在test2中可以ping test1

- 创建bridge
> docker network create -d bridge my-bridge

**当两个docker连接到用户自定义的bridge上时 默认 --link **
```

docker1（namespace1) ----(veth)--docker 0（bridge） --(veth)---docoker2（namespace）
                                  |                              |
                                  |                              |
                                  |                              |
                                 NAT                        my-bridge(自定义)          
                                  |
                                  |
                                 外网

```
- docker Host
端口暴露(portmap)
> -p 宿主机端口：docker端口

**none network**
> docker run -d --name test4 --network none busybox /bin/sh -c "while true; do sleep 3600; done"

none 模式可以做安全机，只允许本地访问的容器

**host network**
> docker run -d --name test5 --network host busybox /bin/sh -c "while true; do sleep 3600; done"

进入test5
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 00:16:3e:65:15:c3 brd ff:ff:ff:ff:ff:ff
    inet 10.101.21.195/24 brd 10.101.21.255 scope global dynamic eth0
       valid_lft 17301sec preferred_lft 17301sec
    inet6 fe80::216:3eff:fe65:15c3/64 scope link 
       valid_lft forever preferred_lft forever
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue 
    link/ether 02:42:22:25:65:26 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:22ff:fe25:6526/64 scope link 
       valid_lft forever preferred_lft forever
49: veth5debf6f@if48: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue master br-8652e66956a3 
    link/ether ba:bf:0e:cd:30:93 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::b8bf:eff:fecd:3093/64 scope link 
       valid_lft forever preferred_lft forever
53: vethbcf87f1@if52: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue master docker0 
    link/ether ae:4f:4e:91:5b:db brd ff:ff:ff:ff:ff:ff
    inet6 fe80::ac4f:4eff:fe91:5bdb/64 scope link 
       valid_lft forever preferred_lft forever


# 接口和宿主机的接口一样，因为和宿主机共享一套network networkspace,可能导致端口有冲突
```
### 多容器复杂应用的部署

一个redis & 一个flask—redis

flask
```python
import socket
import os
from redis import Redis
from flask import Flask
app = Flask(__name__)
redis = Redis(host=os.environ.get('REDIS_HOST','127.0.0.1'),port=6379)
@app.route('/')
def hello():
    redis.incr('hits')
    return 'i have been %s times adn hostname'%(redis.get('hits'))

app.run(host='0.0.0.0',port=5000)
```
Dockfile
```
FROM python:3.6
LABEL maintainer="zhangbin <nateeinit@163.com>"
RUN pip install flask redis -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY app.py /app/
WORKDIR /app
EXPOSE 5000
CMD ["python","app.py"]
```

启动redis 
> docker pull redis
> docker run -d --name redis redis

制作image
> docker build -t natee/flask-redis .

启动flask
> docker run -d -p 5000:5000 --link redis --name flask-redis -e REDIS_HOST=redis natee/flask-redis


**-e 参数给容器设置环境变量**


### 不同linux中，多机器通信(overlay和underlay)

- VXLAN

依赖一个分布式储存
**etcd**

### Docker的持久化存储和数据共享
**使用场景**
容器产生的数据需要保存时：例如容器内使用数据库时

<a href='https://github.com/natee1992/Remark/blob/master/WechatIMG5.png'></a>

- 基于本地文件系统的Volume
- 基于plugin的Volume
 - volume的类型
  - 受管理的data Volume，由docker后台自动创建
  - 绑定挂载的Volume，挂载位置由用户指定



### Docker 部署优势
1. 不用考虑不同机器环境不同问题
2. 生成镜像，pull之后，直接可start运行
3. 方便多服务部署，集群部署docker-compose，或者K8s
4. Dockerfile分层生成，方便修改，将变量放置最后
5. 启动秒级，方便回滚版本

### Docker 核心概念
**镜像image**
镜像是指一个系统的镜像，类似windows的ghost镜像

**性能损耗**
得益于现在的 linux 内核的 namespace， 我们可以拥有各种直达内耗的容器可以用，你在 docker 中的进程其实进程就是直接的宿主机进程，这一切都在系统启动 clone 函数的时候就决定了， 所以谈不上性能损耗。

**容器**
容器是一个镜像image的实例，在运行image后会生成一个实例

**hub**
就是镜像仓库。
如果我们部署，我肯定就要用 dockerhub， 我们把镜像托管到 docker hub 上(当然我们也可以假设，或者是用别人假设的hub)
国内有很多三方 dockerhub 服务器， 有阿里云，网易蜂巢，有容云，daocloud 等等等等
至于国外就是 amazon

### Docker 命令

```

ocker   # docker 命令帮助

Commands:
    attach    Attach to a running container                 # 当前 shell 下 attach 连接指定运行镜像
    build     Build an image from a Dockerfile              # 通过 Dockerfile 定制镜像
    commit    Create a new image from a container's changes # 提交当前容器为新的镜像
    cp        Copy files/folders from the containers filesystem to the host path
              # 从容器中拷贝指定文件或者目录到宿主机中
    create    Create a new container                        # 创建一个新的容器，同 run，但不启动容器
    diff      Inspect changes on a container's filesystem   # 查看 docker 容器变化
    events    Get real time events from the server          # 从 docker 服务获取容器实时事件
    exec      Run a command in an existing container        # 在已存在的容器上运行命令
    export    Stream the contents of a container as a tar archive   
              # 导出容器的内容流作为一个 tar 归档文件[对应 import ]
    history   Show the history of an image                  # 展示一个镜像形成历史
    images    List images                                   # 列出系统当前镜像
    import    Create a new filesystem image from the contents of a tarball  
              # 从tar包中的内容创建一个新的文件系统映像[对应 export]
    info      Display system-wide information               # 显示系统相关信息
    inspect   Return low-level information on a container   # 查看容器详细信息
    kill      Kill a running container                      # kill 指定 docker 容器
    load      Load an image from a tar archive              # 从一个 tar 包中加载一个镜像[对应 save]
    login     Register or Login to the docker registry server   
              # 注册或者登陆一个 docker 源服务器
    logout    Log out from a Docker registry server         # 从当前 Docker registry 退出
    logs      Fetch the logs of a container                 # 输出当前容器日志信息
    port      Lookup the public-facing port which is NAT-ed to PRIVATE_PORT
              # 查看映射端口对应的容器内部源端口
    pause     Pause all processes within a container        # 暂停容器
    ps        List containers                               # 列出容器列表
    pull      Pull an image or a repository from the docker registry server
              # 从docker镜像源服务器拉取指定镜像或者库镜像
    push      Push an image or a repository to the docker registry server
              # 推送指定镜像或者库镜像至docker源服务器
    restart   Restart a running container                   # 重启运行的容器
    rm        Remove one or more containers                 # 移除一个或者多个容器
    rmi       Remove one or more images                 
              # 移除一个或多个镜像[无容器使用该镜像才可删除，否则需删除相关容器才可继续或 -f 强制删除]
    run       Run a command in a new container
              # 创建一个新的容器并运行一个命令
    save      Save an image to a tar archive                # 保存一个镜像为一个 tar 包[对应 load]
    search    Search for an image on the Docker Hub         # 在 docker hub 中搜索镜像
    start     Start a stopped containers                    # 启动容器
    stop      Stop a running containers                     # 停止容器
    tag       Tag an image into a repository                # 给源中镜像打标签
    top       Lookup the running processes of a container   # 查看容器中运行的进程信息
    unpause   Unpause a paused container                    # 取消暂停容器
    version   Show the docker version information           # 查看 docker 版本号
    wait      Block until a container stops, then print its exit code   
              # 截取容器停止时的退出状态值
Run 'docker COMMAND --help' for more information on a command.
```

*docker命令实例*

*docker生成新image*
> docker commit -m 'commit message'  container_id 'name'

*docker复制文件*
> docker cp 文件名  container_id /地址

*docker删除镜像*
> docker rmi image_id

*docker停止容器*
> docker stop comtainer_id 

*docker退出容器不停止*
> ctrl + p + q

*docker进入容器*
> docker exec -it container_id /bin/bash

> ssh root@localhost -p 映射端口号

**docker 外部命令**
查找镜像
> docker search XX

下载镜像
> docker pull X

查看所有镜像
> docker images

删除镜像
> docker rmi

查看所有容器
> docker ps -a

删除容器
> docker rm x

启动容器
> docker run/start

查看日志
> docker logs x

查看最近50行日志
> docker logs -f -t --tail 50 8ffe6610c91a

## Dockerfile
*docker 时区问题+8或者-8*
> RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
> && echo 'Asia/Shanghai' >/etc/timezone

example
```
ROM freedoms1988/centos7-sshd
MAINTAINER zb <xxx@mail.com>

RUN yum install -y gcc
RUN yum install -y epel-release
RUN yum -y update
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u
RUN yum install -y python36u-pip
RUN yum install -y python36u-devel python-devel supervisor

RUN ln -s /bin/python3.6 /bin/python3 && ln -s /bin/pip3.6 /bin/pip3 && mkdir /root/web

COPY requirements.txt /root/web/

RUN pip3 install -r /root/web/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY supervisor.ini /etc/supervisord.d/
COPY web /root/web/
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone

CMD ["/usr/bin/supervisord"]

```
## docker-compose

**简介**
docker-compose 是用来做docker 的多容器控制
docker-compose 是一个用来把 docker 自动化的东西。
有了 docker-compose 你可以把所有繁复的 docker 操作全都一条命令，自动化的完成



