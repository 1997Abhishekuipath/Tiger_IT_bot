from django.contrib import admin
from organization.models.model_organization import Organization
from organization.models.model_organization_user import OrganizationUser


class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]


admin.site.register(Organization, OrganizationAdmin)


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'organization',
        'role'
    ]


admin.site.register(OrganizationUser, OrganizationUserAdmin)
