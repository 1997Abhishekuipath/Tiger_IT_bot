from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from customAuth.models.model_user import User
from customAuth.models.model_permissions import Permission
from customAuth.models.model_role_permissions import PermissionRole
from customAuth.models.model_user_roles import RoleUser
from customAuth.models.model_roles import Role


class UserAdminCustom(UserAdmin):
    fieldsets = (
        # (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(User, UserAdminCustom)


class PermissionRoleInline(admin.TabularInline):
    model = PermissionRole
    extra = 1


class RoleUserInline(admin.TabularInline):
    model = RoleUser
    extra = 1


class PermissionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slug',
        'display_name',
    ]
    inlines = (PermissionRoleInline,)


admin.site.register(Permission, PermissionAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slug',
        'display_name',
        'role_type',
    ]
    inlines = (PermissionRoleInline, RoleUserInline)


admin.site.register(Role, RoleAdmin)


class PermissionRoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'permission',
        'role',
    ]


admin.site.register(PermissionRole, PermissionRoleAdmin)
