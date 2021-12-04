import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.serializers import ValidatorSerializer
from .models import User
from .utils.permissions import set_user_permession


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_permissions(user):
        return user.get_all_permissions()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'permissions')


class LoginValidator(ValidatorSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()

        if user:
            if not user.is_active:
                raise ValidationError({'username': _("Пользователь не активен")})

            if not user.check_password(data.get('password')):
                raise AuthenticationFailed({'password': _("Неверный пароль")})

            return data, user
        else:
            raise AuthenticationFailed({'username': _("Пользователь не существует")})


class LoginDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()


class ChangePasswordSerializer(ValidatorSerializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    temp = random.sample(string.ascii_lowercase + string.digits, 10)
    password = "".join(temp)

    print(password)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # set_user_permession(username=user.username, type=1)

        return user
