from django.db import models
from common.models.model_timestamp import TimestampsModelMixin


class RoleUser(TimestampsModelMixin):
    role = models.ForeignKey(
        'Role',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
