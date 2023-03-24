from django.db import models
from common.models.model_timestamp import TimestampsModelMixin


class PermissionRole(TimestampsModelMixin):
    permission = models.ForeignKey(
        'Permission',
        on_delete=models.CASCADE,
    )

    role = models.ForeignKey(
        'Role',
        on_delete=models.CASCADE,
    )
