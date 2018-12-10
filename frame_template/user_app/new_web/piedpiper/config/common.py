import os
from os.path import join
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        # Third party apps
        'rest_framework',  # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_filters',  # for filtering rest endpoints
        # Your apps
        # 'piedpiper.users',
        'piedpiper.user',

    )
    SITE_ID = 1
    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = 'piedpiper.urls'
    # SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    SECRET_KEY = 'sjkx3tg5u-vvc6thmt_*s&!q1@*)=k6x6p_ogyw_=jd))t!(c_'

    WSGI_APPLICATION = 'piedpiper.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', 'richard.hendriks@piedpiper.com'),
    )

    # Postgres
    DATABASES = {
        # 'default': dj_database_url.config(
        #     default='postgres://postgres:@postgres:5432/postgres',
        #     conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        # )
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'Asia/Shanghai'
    LANGUAGE_CODE = 'zh-hans'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'user.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    # 允许跨域资源共享
    CORS_ORIGIN_ALLOW_ALL = True

    # 配置缓存设置
    REDIS_TIMEOUT = 60 * 15
    CUBES_REDIS_TIMEOUT = 60 * 60
    NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379',
            "OPTIONS": {
                "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            },
            "TIMEOUT": REDIS_TIMEOUT
        },
    }

    # 登录方式 选项
    # option:  name ;  name&mobile ; name&email ; all  ;
    ACCOUNT_AUTHENTICATION_METHOD = 'name&mobile'

    # 设置 是否 启用 session
    REST_SESSION_LOGIN = True

    # 将会话的engine 配置为基于 cookie的会话
    # SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    SESSION_COOKIE_HTTPONLY = True

    # 配置 session 过期时间
    # SESSION_SAVE_EVERY_REQUEST = True
    SESSION_COOKIE_AGE = 30

    # 设置 token 的过期时间 单位 s
    TOKEN_EXPIRE_TIME = 30

    # Json Web Token 配置
    import datetime

    # 设置 是否启用jwt
    # 如果不启用 jwt  则默认使用 token
    REST_USE_JWT = False

    JWT_AUTH = {
        'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=5),
        'JWT_AUTH_HEADER_PREFIX': 'JWT',
    }
