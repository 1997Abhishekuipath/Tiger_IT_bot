from django.db import models
from common.models.model_timestamp import TimestampsModelMixin


class Permission(TimestampsModelMixin):
    slug = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        default=None,
    )

    display_name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return '{} : {} : {}'.format(self.id, self.slug, self.display_name)
