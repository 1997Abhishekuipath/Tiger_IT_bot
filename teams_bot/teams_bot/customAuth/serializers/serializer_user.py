from rest_framework import serializers
from customAuth.models.model_user import User
from customAuth.models.model_permissions import Permission
from customAuth.models.model_role_permissions import PermissionRole


class RegisterFormSerializer(serializers.ModelSerializer):
    invitation_token = serializers.UUIDField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "invitation_token",
            "first_name",
            "last_name",
            "email",
            "password"
        ]


class LoginFormSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserBaseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'token',
            'permissions',
        ]

    def get_permissions(self, obj):
        permission_objs = Permission.objects.filter(
            pk__in=PermissionRole.objects.filter(
                role__in=obj.roles.all()
            ).values_list("permission_id", flat=True)
        )
        return permission_objs.values_list('slug', flat=True)
