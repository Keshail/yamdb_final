from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = [
    ('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username
