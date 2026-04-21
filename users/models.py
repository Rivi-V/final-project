from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from team_finder.constants import (
    SKILL_NAME_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from users.managers import UserManager
from users.utils import generate_avatar_file


class Skill(models.Model):
    name = models.CharField('Название', max_length=SKILL_NAME_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField('Фамилия', max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    phone = models.CharField('Телефон', max_length=USER_PHONE_MAX_LENGTH, blank=True)
    github_url = models.URLField('GitHub', blank=True)
    about = models.CharField('О себе', max_length=USER_ABOUT_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, related_name='users', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        ordering = ('-date_joined', '-id')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar_file(self.name[0])
        super().save(*args, **kwargs)
