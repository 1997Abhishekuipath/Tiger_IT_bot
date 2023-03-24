from django.db import models
from common.models.model_timestamp import TimestampsModelMixin


class OrganizationUser(TimestampsModelMixin):
    organization = models.ForeignKey(
        'organization',
        on_delete=models.CASCADE,
        related_name='organization_users',
    )

    user = models.ForeignKey(
        'customAuth.User',
        on_delete=models.CASCADE,
        related_name='organization_users',
    )

    role = models.ForeignKey(
        'customAuth.Role',
        on_delete=models.SET_NULL,
        null=True,
        related_name='organization_users',
    )

    class Meta:
        unique_together = [['organization', 'user'], ]

    def __str__(self):
        return '{}: {}: {}: {}:'.format(self.id, self.organization , self.user , self.role)
