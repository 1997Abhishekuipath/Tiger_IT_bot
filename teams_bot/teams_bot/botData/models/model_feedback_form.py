from django.db import models
from bot.models.model_bot import Bot
from botPlatform.models.model_botuser import BotUserInfo
from common.models.model_timestamp import TimestampsModelMixin
from botData.models.model_messages import Message


class FeedbackForm(TimestampsModelMixin):
    user_message = models.TextField()
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
        return '{}: {}'.format(self.id, self.user_message)
