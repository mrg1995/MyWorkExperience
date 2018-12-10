###  定时抓取 TIOBE  语言排行榜 

简单抓取TIOBE  月度 前50 语言排行榜,  历年明星语言,以及用于绘制图表的信息,并存入数据库

- Overview

  - python3.6
  - mysql
  - redis

- Install

  1. python 包安装

     ``pip install -r requirements.txt``

  2. redis 安装

     ``sudo apt-get install redis``

  3. mysql 安装

     ``sudo apt-get install mysql-server``

- Quickstart

  1. 在mysql数据中 新增 tiobe数据库

     ``create database tiobe charset=utf8``

  2. 在conifg.py中 修改 数据库连接配置 写入自己的用户名 密码

     ```
     DATABASE_URL = 'mysql://(用户名):(密码)@127.0.0.1:3306/tiobe?charset=utf8mb4'
     ```

  3. 运行

     ``./start.sh``

     ​

  ​