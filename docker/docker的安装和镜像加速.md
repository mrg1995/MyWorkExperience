### 安装docker

#### 开始安装

- 由于apt官方库里的docker版本可能比较旧，所以先卸载可能存在的旧版本：

```
$ sudo apt-get remove docker docker-engine docker-ce docker.io
```

- 更新apt包索引：

```
$ sudo apt-get update
```

- 安装以下包以使apt可以通过HTTPS使用存储库（repository）：

```
$ sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
```

- 添加Docker官方的GPG密钥：

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

- 使用下面的命令来设置**stable**存储库：

```
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

- 再更新一下apt包索引：

```
$ sudo apt-get update
```

- 安装最新版本的Docker CE：

```
$ sudo apt-get install -y docker-ce
```

- 在生产系统上，可能会需要应该安装一个特定版本的Docker CE，而不是总是使用最新版本：

列出可用的版本：

```
$ apt-cache madison docker-ce
```

选择要安装的特定版本，第二列是版本字符串，第三列是存储库名称，它指示包来自哪个存储库，以及扩展它的稳定性级别。要安装一个特定的版本，将版本字符串附加到包名中，并通过等号(=)分隔它们：

```
$ sudo apt-get install docker-ce=<VERSION> # 随意选择一个版本即可 
```

#### 验证docker

- 查看docker服务是否启动：

```
$ systemctl status docker
```

- 若未启动，则启动docker服务：

```
$ sudo systemctl start docker
```

- 经典的hello world：

```
$ sudo docker run hello-world
```

#### 修改配置

- 配置/lib/systemd/system/docker.service

```
$ sudo vim /lib/systemd/system/docker.service
```

这里的0.0.0.0根据自己的需求配置是否只需要配置本地

```
$ ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:4243
```

- 配置/etc/default/docker


```
sudo vim /etc/default/docker
DOCKER_OPTS="-H tcp://localhost:4243 -H unix:///var/run/docker.sock"
```

- DOCKER_HOST的环境变量设置

```
export DOCKER_HOST=tcp://localhost:4243
```

- 添加镜像加速源

```
sudo vim /etc/docker/daemon.json

#添加
{
  "registry-mirrors": ["https://orrpd3b6.mirror.aliyuncs.com"]  
}
```

- 重启docker

```
systemctl daemon-reload
sudo service docker restart
```

