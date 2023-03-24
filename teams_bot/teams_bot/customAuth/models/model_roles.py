from django.db import models
from common.models.model_timestamp import TimestampsModelMixin
from customAuth.models.model_permissions import Permission


class Role(TimestampsModelMixin):
    slug = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        default=None,
    )

    display_name = models.CharField(
        max_length=255,
    )

    role_type = models.CharField(
        max_length=255,
        choices=[
            ['user', 'User'],
            ['organization_user', 'Organization User']
        ],
    )

    permissions = models.ManyToManyField(
        Permission,
        related_name='roles',
        through='PermissionRole',
        blank=True,
    )

    def __str__(self):
        return '{} : {} : {}'.format(self.id, self.slug, self.display_name)
