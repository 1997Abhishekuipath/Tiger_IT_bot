from django.db import models
from django.db.models import JSONField
from common.models.model_timestamp import TimestampsModelMixin


# Create your models here.
class Agent(TimestampsModelMixin):
    nlp_types = [("rasa", "rasa"),
                 ("dialogflow", "dialogflow")]
    name = models.CharField(
        max_length=100,
        null=False
    )
    description = models.CharField(
        max_length=100,
        null=True
    )
    config = JSONField(
        default=dict
    )
    type = models.CharField(
        max_length=20,
        choices=nlp_types
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return '{}: {}: {}'.format(self.id, self.name, self.description)
