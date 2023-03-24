from common.models.model_timestamp import TimestampsModelMixin
from django.db import models


class Organization(TimestampsModelMixin):
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return '{}: {}: '.format(self.id, self.name)
