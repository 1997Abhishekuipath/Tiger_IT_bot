from django.db import models
from django.db.models import JSONField
from bot.models.model_bot import Bot
from common.models.model_timestamp import TimestampsModelMixin


class Intent(TimestampsModelMixin):
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
    bot_id = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)
