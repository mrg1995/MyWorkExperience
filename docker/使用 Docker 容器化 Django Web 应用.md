# 使用 Docker 容器化 Django 应用

在这篇文章中，我将展示如何使用 Docker 容器化现有项目。我从 GitHub 中挑选了一个随机项目，该项目有一个公开的 [issue](https://github.com/shakedown-street/punkweb-boards/issues/66)，称 Docker 化（后文使用 Dockerize）可以在这里作为示例进行贡献和使用。

我决定使用 Docker，因为我的一个应用程序很难部署。有太多的系统依赖，太多的数据库，还有需要单独部署的 Celery 和 rabbitMQ。因此，每当新开发人员加入团队或不得不使用新计算机时，系统的部署都需要很长时间。

部署的麻烦导致时间的损失，而时间损失又导致懒惰，懒惰又导致不良习惯，并这样继续下去……例如，懒可能会使你决定使用 SQLite 而不是 Postgres。

如果你不知道 Docker 是什么，你只需要将它理解成一个巨大的 virtualenv（一种 Python 虚拟环境），它实际上不仅只包含一些 Python 软件包，且使用 Containers（容器）将操作系统中的所有依赖与应用程序，数据库，Worker（译注：应该说的是 Celery Worker） 等等打包结合

### Docker

为了告诉 Docker 如何将您的应用程序作为容器运行，您必须创建一个 Dockerfile：

```
FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /webapps
WORKDIR /webapps
Installing OS DependenciesRUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev

RUN pip install -U pip setuptools

COPY requirements.txt /webapps/
COPY requirements-opt.txt /webapps/

RUN pip install -r /webapps/requirements.txt
RUN pip install -r /webapps/requirements-opt.txt

ADD . /webapps/
Django serviceEXPOSE 8000
```

然后我们一行一行看：

#### Docker 镜像

```
FROM python:3.6
# 在这里，使用来自 Docker Hub 的镜像，它帮助我们建立一个已经安装了 Python3.6 的Ubuntu 容器。
```

#### 环境变量（ENV）

```
# 你可以使用 Env 关键字创建任意的环境变量。
ENV PYTHONUNBUFFERED 1
```

```
# 例如，如果你使用它来存储你的 Django 密钥，你可以这样写：
ENV DJANGO_SECRET_KEY abcde0s&&$uyc)hf_3rv@!a95nasd22e-dxt^9k^7!f+$jxkk+$k-
```

```
# 在你的代码里这样使用：
import os
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

#### 执行命令（RUN）

Docker 运行命令很容易理解。就是在你的容器里面运行一个命令。我在里面引用是因为docker直接将一些依赖完成下载，因此在重建容器时不必再次运行相同的命令。

```
RUN mkdir /webapps
WORKDIR /webapps
Installing OS DependenciesRUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev

RUN pip install -U pip setuptools

COPY requirements.txt /webapps/
COPY requirements-opt.txt /webapps/

RUN pip install -r /webapps/requirements.txt
RUN pip install -r /webapps/requirements-opt.txt

ADD . /webapps/
```

在这种情况下，我们创建用来保存我们项目的 /webapps 目录。

WORKDIR 也是不言而喻的。它只是让 docker 知道后面 RUN 时的目录。

之后，我们安装操作系统依赖项（apt-get 是操作系统的包管理工具），然后安装 Python 依赖项（pip 是 Python 的包管理工具）

#### 复制（COPY）和添加（ADD）

COPY 和 ADD 是相同的。都将您的计算机（主机）中的文件复制到容器中。

#### 暴露端口（EXPOSE）

EXPOSE 指令用于将端口从 Docker 内映射到主机。

```
# Django service
EXPOSE 8000
```

好了，现在怎么样？但是我们如何添加更多容器并使它们一起工作？比如在容器中还需要 PostgreSQL 呢？别担心，我们继续往下看

#### Docker-Compose

Docker-compose 是一个用于运行多个 Docker 容器的工具。表征是一个 yml 文件，你只需要在你的项目文件夹中创建一个 docker-compose.yml 文件。

```
version: '3.3'

services:
# Postgres
db:
  image: postgres
  environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - POSTGRES_DB=postgres

web:
  build: .
  command: ["./run_web.sh"]
  volumes:
    - .:/webapps
  ports:
    - "8000:8000"
  links:
    - db
  depends_on:
    - db
```

 在这里，我使用 Docker Hub 中的 [Postgres 镜像](https://hub.docker.com/_/postgres/)。

现在，让我们更改 settings.py 以配置 Postgres 作为数据库。

```
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'db',
    'PORT': '5432',
}
} 
```

我们差不多完成了。我来谈谈一下 docker-compose 文件。

#### 卷（VOLUMES）

当您在共享卷上写入文件时，该文件也正在写入您的容器中。

```
volumes:
- .:/webapps
```

在这，当前目录（.）将作为 /webapps 目录在容器上共享。

#### LINKS

```
links:
- db
```

您可以使用其名称引用你的另一个容器。既然我们为我们的 Postgres 创建了一个 db 容器，我们可以将它连接到我们的 web 容器上。你可以在我们的 settings.py 文件中看到我用 'db' 作为 HOST。（这里蛮神奇的）

#### DEPENDS_ON

为了你的应用程序正常工作，你的数据库必须在 web 容器之前准备好，否则会引发异常。

```
depends_on:
- db
```

#### Command

Command 是容器在启动后立即运行的默认命令。

对于我们的示例，我创建了一个 run_web.sh 脚本，它将运行迁移（migrations），收集静态文件并启动开发服务器。

```
#!/usr/bin/env bash

cd django-boards/
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
```

每次容器启动都自动运行迁移不是一个好习惯。我也同意，你可以直接在网络机器上运行它。

```
docker-compose run web bash
```

如果希望可以在不访问容器本身的情况下运行它，只需更改上一个命令的最后一个参数 bash 即可，如：

```
docker-compose run web python manage.py migrate
```

其它命令也一样：

```
docker-compose run web python manage.py test
docker-compose run web python manage.py shell
```

#### 运行 Docker

我们的 Dockerfile，docker-compose.yml 和 run_web.sh 已经就位了，我们可以一起运行它们：

```
docker-compose up
```

 [原文链接](http://dockone.io/article/3656)