from django.conf import settings

from .serializers import (
    TokenSerializer as DefaultTokenSerializer,
    JWTSerializer as DefaultJWTSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
    PasswordChangeSerializer as DefaultPasswordChangeSerializer,
    RegisterSerializer as DefaultRegisterSerializer)
from .utils import import_callable, default_create_token

from rest_framework.permissions import AllowAny


serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})

RegisterSerializer = import_callable(
    serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))


def register_permission_classes():
    permission_classes = [AllowAny, ]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))
    return tuple(permission_classes)


create_token = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

JWTSerializer = import_callable(
    serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))

UserDetailsSerializer = import_callable(
    serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)

PasswordResetSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_SERIALIZER',
        DefaultPasswordResetSerializer
    )
)

PasswordResetConfirmSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_CONFIRM_SERIALIZER',
        DefaultPasswordResetConfirmSerializer
    )
)

PasswordChangeSerializer = import_callable(
    serializers.get(
        'PASSWORD_CHANGE_SERIALIZER',
        DefaultPasswordChangeSerializer
    )
)
