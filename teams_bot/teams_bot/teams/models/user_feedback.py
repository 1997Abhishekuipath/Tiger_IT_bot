from django.db import models
from django.db.models import JSONField


# Create your models here.
class UserFeedback(models.Model):
    username = models.CharField(
        max_length=255,
        null=False
    )
    feedback = models.TextField(
        null=True,
        blank=True,
    )
    useremail = models.CharField(
        max_length=255,
        null=False
    )

    def __str__(self):
        return '{}: {}: {}:'.format(self.id, self.useremail, self.feedback)
