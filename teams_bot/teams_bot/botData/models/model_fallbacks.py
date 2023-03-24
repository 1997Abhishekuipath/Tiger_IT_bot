from django.db import models
from botData.models.model_messages import Message, BotUserInfo, Bot
from common.models.model_timestamp import TimestampsModelMixin


class FallbackMessage(TimestampsModelMixin):
    bot_id = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        BotUserInfo,
        on_delete=models.CASCADE
    )
    message_id = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{}: {}: {}:'.format(self.id, self.message_id, self.user_id)
