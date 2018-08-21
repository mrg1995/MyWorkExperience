## Request  

### request 解析

drf 中的 request 对象提供了灵活的请求解析,允许使用json data 或其他 media types 像通常处理表单数据一样处理请求

#### .data

返回请求主题的解析内容,跟标准的request.POST和request.FILES 类似,并且还有以下特点:

- 包括所有的解析内容,文件(file)和 非文件
- 支持解析POST以外的HTTP method  比如 PUT  ,PATCH
- 更加灵活,不仅仅支持表单数据,传入同样的JSON数据 一样可以正确解析,并且不用做额外的处理(不管前端提交的是表单数据,还是JSON数据,request.data都能正确解析)

#### .query_params

request.query_params等同与request.GET, 不过名字更加容易理解

request.query_params使代码更加清晰可读,因为任何HTTP method 类型都可以包含查询参数(query parameters) , 而不仅仅是GET 请求

#### .parsers

`APIView` 类或者 `@api_view` 装饰器将根据视图上设置的 `parser_classes` 或 `settings` 文件中的 `DEFAULT_PARSER_CLASSES` 设置来确保此属性（`.parsers`）自动设置为 `Parser` 实例列表。

**通常不需要关注该属性......**

可以打印出来看看，包含三个解析器 `JSONParser`，`FormParser`，`MultiPartParser`。

```bash
[<rest_framework.parsers.JSONParser object at 0x7fa850202d68>, <rest_framework.parsers.FormParser object at 0x7fa850202be0>, <rest_framework.parsers.MultiPartParser object at 0x7fa850202860>]
```

>注意： 如果客户端发送格式错误的内容，则访问 `request.data` 可能会引发 `ParseError` 。默认情况下， REST framework 的 `APIView` 类或者 `@api_view` 装饰器将捕获错误并返回 `400 Bad Request` 响应。 如果客户端发送的请求内容无法解析（不同于格式错误），则会引发 `UnsupportedMediaType` 异常，默认情况下会被捕获并返回 `415 Unsupported Media Type` 响应。

###内容协商

请求公开一些属性,允许确定内容协商阶段的结果.  这样可以实施一些行为,例如给不同的媒体类型选择不同的序列化方案

#### .accepted_renderer

渲染器实例是由内容协商阶段选择的

#### .accepted_media_type

表示内容协商阶段接受的 media_type 的字符串

## [认证（Authentication）](http://drf.jiuyou.info/#/drf/requests?id=%e8%ae%a4%e8%af%81%ef%bc%88authentication%ef%bc%89)

REST framework 提供了灵活的认证方式：

- 可以在 API 的不同部分使用不同的认证策略。
- 支持同时使用多个身份验证策略。
- 提供与传入请求关联的用户（user）和令牌（token）信息。

### [.user](http://drf.jiuyou.info/#/drf/requests?id=user)

`request.user` 通常会返回 `django.contrib.auth.models.User` 的一个实例，但其行为取决于正在使用的身份验证策略。

如果请求未经身份验证，则 `request.user` 的默认值是 `django.contrib.auth.models.AnonymousUser` 的实例（就是匿名用户）。

*关于 .user 的更多内容，以后再说～*

### [.auth](http://drf.jiuyou.info/#/drf/requests?id=auth)

`request.auth` 返回任何附加的认证上下文（authentication context）。`request.auth` 的确切行为取决于正在使用的身份验证策略，但它通常可能是请求经过身份验证的令牌（token）实例。

如果请求未经身份验证，或者没有附加上下文（context），则 `request.auth` 的默认值为 `None`。

*关于 .auth 的更多内容，以后再说～*

### [.authenticators](http://drf.jiuyou.info/#/drf/requests?id=authenticators)

`APIView` 类或 `@api_view` 装饰器将确保根据视图上设置的 `authentication_classes`或基于 `settings` 文件中的 `DEFAULT_AUTHENTICATORS` 设置将此属性（`.authenticators`）自动设置为 `Authentication` 实例列表。

**通常不需要关注该属性......**

> 注意：调用 `.user` 或 `.auth` 属性时可能会引发 `WrappedAttributeError` 异常。这些错误源于 authenticator 作为一个标准的 `AttributeError` ，为了防止它们被外部属性访问修改，有必要重新提升为不同的异常类型。Python 无法识别来自 authenticator 的 `AttributeError`，并会立即假定请求对象没有 `.user` 或 `.auth` 属性。authenticator 需要修复。

多说几句

`.authenticators` 其实存的就是当前使用的认证器（authenticator）列表，打印出来大概是这样：

```
[<rest_framework.authentication.SessionAuthentication object at 0x7f8ae4528710>, <rest_framework.authentication.BasicAuthentication object at 0x7f8ae45286d8>]
```

可以看到这里使用的认证器（authenticator）包括 `SessionAuthentication` 和 `BasicAuthentication`。

## [浏览器增强](http://drf.jiuyou.info/#/drf/requests?id=%e6%b5%8f%e8%a7%88%e5%99%a8%e5%a2%9e%e5%bc%ba)

REST framework 支持基于浏览器的 `PUT`，`PATCH`，`DELETE` 表单。

### [.method](http://drf.jiuyou.info/#/drf/requests?id=method)

`request.method` 返回请求 HTTP 方法的大写字符串表示形式。如 `GET`,`POST`...。

透明地支持基于浏览器的 `PUT`，`PATCH` 和 `DELETE` 表单。

*更多相关信息以后再说～*

### [.content_type](http://drf.jiuyou.info/#/drf/requests?id=content_type)

`request.content_type` 返回表示 HTTP 请求正文的媒体类型（media type）的字符串对象（比如： `text/plain` , `text/html` 等），如果没有提供媒体类型，则返回空字符串。

通常不需要直接访问此属性，一般都依赖与 REST 框架的默认请求解析行为。

不建议使用 `request.META.get('HTTP_CONTENT_TYPE')` 来获取 content type 。

*更多相关信息以后再说～*

### [.stream](http://drf.jiuyou.info/#/drf/requests?id=stream)

`request.stream` 返回一个代表请求主体内容的流。

通常不需要直接访问此属性，一般都依赖与 REST 框架的默认请求解析行为。

## [标准的 HttpRequest 属性](http://drf.jiuyou.info/#/drf/requests?id=%e6%a0%87%e5%87%86%e7%9a%84-httprequest-%e5%b1%9e%e6%80%a7)

由于 REST framework 的 `Request` 扩展于 Django 的 `HttpRequest`，所有其他标准属性和方法也可用。例如`request.META` 和 `request.session` 字典都可以正常使用。

请注意，由于实现原因，`Request` 类不会从 `HttpRequest` 类继承，而是使用组合扩展类（优先使用组合，而非继承，恩，老铁没毛病 0.0）