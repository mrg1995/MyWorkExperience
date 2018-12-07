# -*- coding:utf-8 -*-
__author__ = 'xiaodong Guo'
import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import SessionAuthentication

# 自定义用户认证
# 本来应该是在setting中 配置 AUTHENTICATION_BACKENDS  类似于下面的 将自定义的认证方式类 放到元祖中
# AUTHENTICATION_BACKENDS = (
#     'user.views.MyUserBackend',
# )
# 但是这里是使用Configuration 来配置setting
# 不知道为什么一直报错 只能这样来实现自定义用户认证了

User = get_user_model()

ACCOUNT_AUTHENTICATION_METHOD = settings.ACCOUNT_AUTHENTICATION_METHOD


def authenticate(username=None, password=None, **kwargs):
    try:
        if ACCOUNT_AUTHENTICATION_METHOD == 'name':
            user = User.objects.get(username=username)
        elif ACCOUNT_AUTHENTICATION_METHOD == 'name&mobile':
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        elif ACCOUNT_AUTHENTICATION_METHOD == "name&email":
            user = User.objects.get(Q(username=username) | Q(email=username))
        elif ACCOUNT_AUTHENTICATION_METHOD == "all":
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
        else:
            # 默认只使用用户名登录
            user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except Exception as e:
        return None


# SessionAuthentication 会强行验证csrf
# 重写一个类继承SessionAuthentication, 并关闭csrf验证
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# 获取请求头里的token信息
def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


# 因为 自带的 TokenAuthentication 认证方式不支持过期时间  因此自定义一个支持过期时间验证的token认证方式
# 自定义的ExpiringTokenAuthentication认证方式  基本上模仿TokenAuthentication源码的写法  加了过期 和 缓存的功能
class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None
        try:
            token = auth.decode()
            # 如果 认证 不是 token 认证 而是 jwt认证
            if token[:5].upper() != 'TOKEN':
                return None
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        # 增加了缓存机制
        # 首先先从缓存中查找
        key = key[6:]
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)
        if cache_user:
            return (cache_user.user, cache_user)  # 首先查看token是否在缓存中，若存在，直接返回用户
        try:
            token = self.model.objects.get(key=key)

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('用户未激活')

        utc_now = datetime.datetime.utcnow()

        # 在这里控制 token的过期时间
        if (utc_now.replace(tzinfo=pytz.timezone("UTC")) - token.created.replace(
                tzinfo=pytz.timezone("UTC"))).total_seconds() > settings.TOKEN_EXPIRE_TIME:  # 设定存活时间
            # 如果过期了就把 缓存 和 数据库中的 token 数据删除
            token.delete()
            cache.delete("token_"+key)
            raise exceptions.AuthenticationFailed('认证信息过期')

        if token:
            token_cache = 'token_' + key
            cache.set(token_cache, token, 24 * 7 * 60 * 60)  # 添加 token_xxx 到缓存
        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'
