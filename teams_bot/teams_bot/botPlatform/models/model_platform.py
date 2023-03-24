from common.models.model_timestamp import TimestampsModelMixin
from django.db import models
from bot.models.model_bot import Bot
from django.db.models import JSONField


class Platform(TimestampsModelMixin):
    name = models.CharField(
        max_length=255
    )
    bot_id = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE
    )
    config = JSONField(
        default=dict
    )

    def __str__(self):
        return '{}: {}: {}: {}: '.format(self.id, self.name, self.bot_id, self.config)
