from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    """
    Кастомный класс пользователей.
    Email - обязательное поле. Добавлено свойство "role".
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
        unique=True
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.CharField(max_length=100, blank=True, null=False)


class CustomUserManager(BaseUserManager):
    """Кастомный класс для создания пользователей администратором."""

    def create_user(self, username, email, role):
        """
        Создает пользователя с указанными username и email.
        Присваивает роль.
        """

        if not (email or username):
            raise ValueError('Users must have both username and email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=User.USER if not role else role
        )

        user.save(using=self._db)
        return user
