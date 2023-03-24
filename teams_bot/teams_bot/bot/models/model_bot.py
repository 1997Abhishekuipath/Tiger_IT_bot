from django.db import models
import uuid
from bot.models.model_nlp_agent import Agent
from common.models.model_timestamp import TimestampsModelMixin
from organization.models.model_organization import Organization


class Bot(TimestampsModelMixin):
    name = models.CharField(
        max_length=255
    )
    organization_id = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )
    nlp_agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE
    )
    web_uid = models.UUIDField(
        unique=True,
        null=False,
        default=uuid.uuid4,
    )

    def __str__(self):
        return '{}: {}: '.format(self.id, self.name)
