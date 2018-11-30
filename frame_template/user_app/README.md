#### settings 中的配置 

```
REST_USE_JWT   默认为False  如果改成true token的形式会变成 jwt 
REST_SESSION_LOGIN  默认是 True
ACCOUNT_LOGOUT_ON_GET  默认 False  改成True 则可以用 post  或 get 去请求 登出视图


allauth 里的配置
USERNAME_BLACKLIST  用户名黑名单   在 allauth的 adapter中 有函数 对其做判断
PASSWORD_MIN_LENGTH  密码的长度


# 自己新增的功能
CSRF_EXCEPT    在开发过程中 调试接口 把csrftoken 屏蔽掉
ACCOUNT_AUTHENTICATION_METHOD  登录方式  用户名  邮箱 手机号  
```



```
pip install django-cors-headers
```



