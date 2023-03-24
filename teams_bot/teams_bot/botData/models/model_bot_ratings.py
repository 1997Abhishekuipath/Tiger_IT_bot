from django.db import models

from bot.models.model_bot import Bot
from botPlatform.models.model_botuser import BotUserInfo
from common.models.model_timestamp import TimestampsModelMixin


class BotRating(TimestampsModelMixin):
    rating = models.CharField(
        max_length=10
    )
    bot_id = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        BotUserInfo,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{}: {}'.format(self.id, self.rating)
