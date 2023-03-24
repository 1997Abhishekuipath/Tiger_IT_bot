from django.db import models
from django.db.models import JSONField

from botPlatform.models.model_platform import Platform
from common.models.model_timestamp import TimestampsModelMixin


class BotUserInfo(TimestampsModelMixin):
    name = models.CharField(
        max_length=255,
        null=False
    )
    platform_id = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
    )
    info = JSONField(
        default=dict
    )
    email = models.CharField(
        max_length=255,
        null=False
    )

    def __str__(self):
        userProfile={'id':self.id,'name':self.name,'platform_id':self.platform_id,'email':self.email,'info':self.info}
        return str(userProfile)
    #     return '{}: {}: {}: {}:{}'.format(self.id,self.name, self.platform_id,self.email, ,self.info)
 
        
        