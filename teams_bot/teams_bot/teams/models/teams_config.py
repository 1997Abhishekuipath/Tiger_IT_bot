from django.db import models
from django.db.models import JSONField


# Create your models here.
class TeamsConfig(models.Model):
    app_id = models.CharField(
        max_length=255,
        null=False
    )
    access_token = models.TextField(
        null=True,
        blank=True,
    )
    app_secret = models.CharField(
        max_length=255,
        null=False
    )

    def __str__(self):
        return '{}: {}'.format(self.id, self.app_id)

