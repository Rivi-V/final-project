from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder.constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_MAX_LENGTH,
    PROJECT_STATUS_OPEN,
)
from users.models import Skill


class Project(models.Model):
    STATUS_OPEN = PROJECT_STATUS_OPEN
    STATUS_CLOSED = PROJECT_STATUS_CLOSED
    STATUS_CHOICES = PROJECT_STATUS_CHOICES

    name = models.CharField('Название', max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    github_url = models.URLField('GitHub', blank=True)
    status = models.CharField(
        'Статус',
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_projects',
        blank=True,
    )
    interested_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorites',
        blank=True,
    )
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)

    class Meta:
        ordering = ('-created_at', '-id')
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:detail-no-slash', kwargs={'project_id': self.pk})
