from django.db import models
from django.db.models import JSONField
import datetime
from django.utils import timezone


# Create your models here.
class ConversationParameters(models.Model):
    conversation_id = models.CharField(
        max_length=255,
        null=False
    )
    parameters = JSONField(
        blank=True,
        null=True,
    )
    time = models.DateTimeField(
        default=datetime.datetime.now(),
        null=False
    )

    def __str__(self):
        return '{}: {}: {}'.format(self.id, self.parameters, self.conversation_id)
