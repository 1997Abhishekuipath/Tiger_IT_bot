from django.db import models
from django.db.models import JSONField


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(
        max_length=255,
        null=False
    )
    teams_id = models.CharField(
        max_length=255,
        null=False,
    )
    aad_id = models.CharField(
        max_length=255,
        null=False,
    )
    email_address = models.CharField(
        max_length=255,
        null=False
    )

    def __str__(self):
        return '{}: {}: {}'.format(self.id, self.name, self.email_address)
