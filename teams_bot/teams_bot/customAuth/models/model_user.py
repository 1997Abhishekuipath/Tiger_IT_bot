from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from common.models.model_timestamp import TimestampsModelMixin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser, TimestampsModelMixin):
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=False,
        default=None,
    )

    roles = models.ManyToManyField(
        'Role',
        related_name='users',
        through='RoleUser',
        blank=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return '{} : {}'.format(self.pk, self.email)
