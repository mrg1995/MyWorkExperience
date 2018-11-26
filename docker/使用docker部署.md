#### 使用docker部署

##### 使用docker的原因

1. 将软件环境与linux环境分隔开(例如py3和py2)
2. 可以现在本地调试, 然后直接打包docker为文件, 传到云服务器上, 不用从0配置环境
3. 不会破坏服务器的环境, 删除时只需要删除docker的容器与容器关联的文件夹即可

##### 我们需要的环境

1. 需要mysql5.7镜像
2. 需要python3.6+py包环境(requirements.py)
3. 需要nginx镜像

##### 准备工作

1. 准备一个磁盘空间大一些的虚拟机, 配置好网卡, 桥接
2. 安装docker `yum -y install docker`
3. 启动docker服务 `systemctl start docker`
4. 关闭防火墙 `ststemctl stop firewalld`

##### mysql镜像

1. 拉取镜像 `docker pull mysql:5.7`
2. 测试
   - 创建mysql容器 `docker run -it -d --name=testmysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7` 这里你可修改的值有, name(容器名), 外部端口:内部端口(内部端口默认为3306, 外部端口任意), 数据库root账户的密码
   - 现在就可以使用navicat访问了`centos的ip:4000`
   - 访问成功后, 关闭并删除这个测试用的mysql容器 `docker stop testmysql && docker rm testmysql`

##### nginx镜像

1. 拉取镜像(版本使用官网的稳定版本) `docker pull nginx:1.14`
2. 测试
   - 创建nginx容器 `docker run -it -d --name=testnginx -p 4001:80 nginx:1.14`
   - 在浏览器访问 `http://192.168.3.31:4001/`
   - 看到nginx主页后, 关闭并删除这个测试用的mysql容器 `docker stop testnginx && docker rm testnginx`

##### 配置python3镜像

1. py3不同于上面的两个镜像, 我们需要将我们需要的包配置到容器中, 然后再生成镜像保存下来供之后使用
2. 拉取镜像(版本3.6) `docker pull python:3.6`
3. 创建python容器 `docker run -it -d --name=testpython python:3.6`
4. 进入python容器 `docker exec -it testpython bash`
5. 配置python源(需要你的centos有python源的配置文件)
   - 创建文件夹 `mkdir ~/.pip/`
   - 将centos的pip配置文件复制给docker容器 (在centos的终端中使用, `exit`可退出容器终端)`docker cp ~/.pip/pip.conf testpython:/root/.pip/pip.conf`
6. 将python包文件复制给docker容器
   - 这是我包文件在centos上的位置`/opt/sites/EduOnline/requirements`
   - `docker cp /opt/sites/EduOnline/requirements testpython:/opt/requirements`
7. 在容器的终端执行 `pip install -r /opt/requirements`
8. (在centos的终端)创建新的镜像 `docker commit -m "add python packages" -a "dyq666" testpython py3.6_django2.0`
9. 删除当前容器 `docker stop testpython && docker rm testpython`
10. 删除老的python镜像 `docker image rm python:3.6`
11. 测试新的镜像
    - `docker run -it -d --name=testpydjango py3.6_django2.0`
    - `docker exec -it testpydjango bash`
    - 使用`pip list`和`cat /root/.pip/pip.conf`观察是否成功配置
    - 成功后, 关闭并删除测试容器 `docker stop testpydjango && docker rm testpydjango`

##### 将三个镜像导出

1. 现在我们有了三个可用的镜像, 我们将它们导出, 之后在服务器上导入就可以使用了

2. 将三个镜像导出(会有些慢, 如果磁盘不够使用

   ```
   df -lh
   ```

   找一个大的地方)

   - `docker image save mysql:5.7 -o /opt/dockerimages/mysql5.7.tar`
   - `docker image save nginx:1.14 -o /opt/dockerimages/nginx1.14.tar`
   - `docker image save py3.6_django2.0 -o /opt/dockerimages/py36.django2.tar`

##### 通过docker搭建项目

1. 加载镜像

   - 可以创建一个新的虚拟机模拟一次服务器
   - 将压缩文件放入服务器中, 使用docker导入`docker load -i 压缩的文件`
   - 加载完后删除这些压缩文件

2. 创建mysql容器

   - 创建卷 `docker volume create mysql_v`
   - 创建容器 `docker run -it -d --name=edu_mysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=123456 -v mysql_v:/var/lib/mysql --privileged mysql:5.7`
   - 通过`centos的ip:4000`访问数据库

3. 创建python容器

   - 创建卷 `docker volume create python_v`
   - 创建容器 `docker run -it -d --name=edu_python -p 4001:8000 -v python_v:/opt/sites/ --privileged py3.6_django2.0`
   - 将代码放入卷的目录, 查看目录`docker inspect python_v`

4. 创建docker卷用于存放django的源码 `docker volume python_v`

5. 将django代码移动到docker卷下

   - 我的源码存放在`/opt/sites/EduOnline/`
   - 通过 `docker inspect python_v`查看卷的位置
   - `cp -r /opt/sites/EduOnline/ /var/lib/docker/volumes/python_v/_data/`

6. 调整数据库

   - (centos终端)自行更改配置文件, 将配置文件指向数据库
   - 在navicat中远程连接到数据库, 创建django配置文件中指定的数据库
   - `python manage.py migrate`
   - 自己想办法模拟数据, 我采用py的代码模拟 `python db_mock.py`

7. 运行py `python manage.py runserver 0.0.0.0:8000` (应该去配置gunicorn或uwsgi, 这里仅用于测试)

8. 测试 `ip:4001`, 因为没配置nginx所以没有样式

9. 创建nginx容器

   - `docker run -it -d --name=edu_nginx -v python_v:/opt/sites/ --net=host --privileged nginx:1.14`
   - nginx配置文件, 让nginx帮忙处理static, 其他交给django(192.168.3.40是我虚拟机centos的ip)

   ```
    server {
        listen       4002;
        server_name  192.168.3.40;

        location /static {
            alias /opt/sites/EduOnline/static;
        }

        location /media {
            alias /opt/sites/EduOnline/media;
        }

        location / {
            proxy_pass  http://192.168.3.40:4001;
        }
    }
   ```

   - 把配置文件考到容器内 `docker cp /opt/nginx/django.conf edu_nginx:/etc/nginx/conf.d/django.conf`
   - 进入nginx容器中, 重启nginx