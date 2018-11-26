use mysql;
select host, user from user;
-- 因为mysql版本是5.7，因此新建用户为如下命令：  用户名 test_user  密码 123456
create user test_user identified by '123456';
-- 将docker_mysql数据库的权限授权给创建的docker用户，密码为123456：
grant all on *.* to test_user@'%' identified by '123456' with grant option;
-- 这一条命令一定要有：
flush privileges;