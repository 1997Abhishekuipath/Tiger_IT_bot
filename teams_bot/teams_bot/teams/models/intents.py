from django.db import models
from django.db.models import JSONField


# Create your models here.
class Intent(models.Model):
    name = models.CharField(
        max_length=100,
        null=False
    )
    response = JSONField(
        blank=True,
        null=True,
    )
    webhook = JSONField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)

