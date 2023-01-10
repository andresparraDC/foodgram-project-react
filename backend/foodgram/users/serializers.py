from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import (
    UserSerializer, UserCreateSerializer, SetPasswordSerializer,
)


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD, settings.USER_ID_FIELD
                  ) + tuple(User.REQUIRED_FIELDS)
        read_only_fields = (settings.LOGIN_FIELD,)


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD,
                  settings.USER_ID_FIELD,
                  "password",
                  # 'is_subscribed',
                  ) + tuple(User.REQUIRED_FIELDS)


class CustomSetPasswordSerializer(SetPasswordSerializer):
    class Meta:
        fields = ('password',)
