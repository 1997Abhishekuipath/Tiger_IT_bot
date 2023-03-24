import uuid

from common.models.model_timestamp import TimestampsModelMixin
from django.db import models
from bot.models.model_bot import Bot


class WebBot(TimestampsModelMixin):
    bot_id = models.ForeignKey(
        Bot,
        null=True,
        on_delete=models.SET_NULL
    )
    web_uid = models.UUIDField(
        unique=True,
        null=False,
        default=uuid.uuid4,
    )

    def __str__(self):
        return '{}: {}: {}: '.format(self.id, self.bot_id, self.web_uid)
