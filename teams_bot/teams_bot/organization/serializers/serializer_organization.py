from rest_framework import serializers
from organization.models import Organization, OrganizationUser


class OrganizationSerializer(serializers.ModelSerializer):
    # permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
        ]

    def get_permissions(self, obj):
        print(self.context['request'].user)
        permission_objs = OrganizationUser.objects.filter(
            organization=obj,
            user=self.context['request'].user,
        ).first().role.permissions.all()
        print("permission_obj", permission_objs)
        return permission_objs.values_list('slug', flat=True)
