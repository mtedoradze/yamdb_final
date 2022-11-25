from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import UserPermission
from .models import User


class CustomPasswordField(PasswordField):
    """Переопределение поля password на confirmation_code"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'confirmation_code'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class CustomTokenObtainSerializer(serializers.Serializer):
    """Переопределение сериализатора для получения токена"""

    username_field = User.USERNAME_FIELD
    token_class = AccessToken
    default_error_messages = {
        "no_active_account": "Такого пользователя нет"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = CustomPasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["confirmation_code"],
        }

        if not self.context.get("request"):
            raise exceptions.ParseError

        self.user = authenticate(**authenticate_kwargs)

        if not User.objects.filter(username=attrs[self.username_field]):
            raise exceptions.NotFound
        if not User.objects.filter(password=attrs["confirmation_code"]):
            raise exceptions.ParseError

        token = AccessToken.for_user(self.user)
        return {'token': str(token)}


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя с username и email."""

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено')
        return data

    def create(self, validated_data):
        password = User.objects.make_random_password()
        email = self.validated_data['email']
        user = User.objects.create_user(
            password=password,
            role='user',
            **validated_data
        )
        user.save()
        send_mail(
            'Подтверждение регистрации',
            f'для пользователя {user.username} '
            f'confirmantion_code: {password}',
            None,
            [f'{email}'],
            fail_silently=False,
        )
        return user


class UserAdminCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и управления пользователями."""

    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default=User.USER
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        name = data.get('username')

        if name and name.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return data


class UserSelfUpdateSerializer(UserAdminCreateSerializer):
    """
    Сериализатор для изменения данных своей учетной записи.
    Поле role - только для чтения.
    """
    role = serializers.CharField(read_only=True)
    permission_classes = [UserPermission]
