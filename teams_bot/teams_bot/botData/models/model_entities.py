from django.db import models
from django.db.models import JSONField

from bot.models.model_bot import Bot


# Create your models here.
class Entity(models.Model):
    entity_key = models.CharField(
        max_length=255,
        null=False
    )
    entity_synonyms = JSONField(
        default=list,
        blank=True,
        null=True,
    )
    entity_value = models.CharField(
        max_length=255,
        null=False
    )
    bot_id = models.ManyToManyField(
        Bot
    )

    def __str__(self):
        return '{}: {}: {}: {}: {}'.format(self.id, self.entity_key, self.entity_value, self.entity_synonyms,
                                           self.bot_id)
