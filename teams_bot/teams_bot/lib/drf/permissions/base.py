from rest_framework import permissions, exceptions
from customAuth.models.model_permissions import Permission
from customAuth.models.model_role_permissions import PermissionRole
from organization.models.model_organization_user import OrganizationUser


class IsOrganizationMember(permissions.BasePermission):
    def has_permission(self, request, view):
        organization_id = request.query_params.get('organization')
        organization = request.user.organizations.filter(pk=organization_id).first()
        if not organization:
            raise exceptions.PermissionDenied("Invalid organization")
        request.organization = organization
        return True


class ValidatePermissionSet(permissions.BasePermission):
    def has_permission(self, request, view):
        print("permission request", request, view)
        if not hasattr(view, 'permission_set'):
            return False
        if view.permission_set.__class__ == dict:
            permissions_to_be_validated = view.permission_set[request.method]
        elif view.permission_set.__class__ == list:
            permissions_to_be_validated = view.permission_set
        else:
            permissions_to_be_validated = None
        if permissions_to_be_validated.__class__ == list:
            if not hasattr(request, 'organization') and request.query_params.get('organization'):
                organization_id = request.query_params.get('organization')
                organization = request.user.organizations.filter(pk=organization_id).first()
                request.organization = organization
            if hasattr(request, 'organization'):
                permission_objs = OrganizationUser.objects.filter(
                    organization=request.organization,
                    user=request.user,
                ).first().role.permissions.all()
            else:
                permission_objs = Permission.objects.filter(
                    pk__in=PermissionRole.objects.filter(
                        role__in=request.user.roles.all()
                    ).values_list("permission_id", flat=True)
                )
            all_permissions = permission_objs.values_list('slug', flat=True)
            if set(permissions_to_be_validated).issubset(all_permissions):
                return True
        return False
