import os


from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):

    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=piedpiper'
    ]

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


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
            # 自己调试的时候 把 CSRF给禁用掉
            # 'rest_framework.authentication.SessionAuthentication',
            'piedpiper.user.authenticate.CsrfExemptSessionAuthentication',
            'piedpiper.user.authenticate.ExpiringTokenAuthentication',
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        )
    }



