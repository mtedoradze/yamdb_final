from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        help_text='Введите жанр',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        help_text='Введите ссылку',
        unique=True,
        db_index=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        help_text='Введите категорию',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        help_text='Введите ссылку',
        unique=True,
        db_index=True,
    )

    def __str__(self):
        return self.name


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError('year cannot be greater than the current year')


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Введите год выпуска',
        null=True,
        blank=True,
        validators=[year_validator]
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание',
        null=True,
        blank=True
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Выберите жанр',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Выберите категорию',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(0, 'Оценка 1-10'),
            MaxValueValidator(10, 'Оценка 1-10'),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
