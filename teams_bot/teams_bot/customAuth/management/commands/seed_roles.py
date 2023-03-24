from django.db import transaction
from django.core.management.base import BaseCommand
from customAuth.models.model_roles import Role, Permission
from customAuth.models.model_role_permissions import PermissionRole


class Command(BaseCommand):
    help = 'seed roles'

    def handle(self, *args, **options):
        with transaction.atomic():
            roles_data = [
                {
                    'slug': 'Normal User',
                    'display_name': 'Normal',
                    'role_type': 'user',
                    'permissions': ['organization.view', 'organization.dashboard.view']
                },
                {
                    'slug': 'user_super_admin',
                    'display_name': 'Super Admin',
                    'role_type': 'user',
                    'permissions': ['bot.view', 'bot.add', 'bot.change', 'bot.delete', 'agent.view', 'agent.add',
                                    'agent.change', 'agent.delete', 'organization.dashboard.view',
                                    'organization_user.view', 'organization.add', 'organization_user.change',
                                    'organization_user.delete', 'organization.change', 'organization.delete',
                                    'organization.dashboard.view', 'organization_user.view',
                                    'organization_user.add', 'organization_user.change', 'organization_user.delete']
                },
                {
                    'slug': 'organization_reviewer',
                    'display_name': 'Reviewer',
                    'role_type': 'organization_user',
                    'permissions': ['bot.view', 'agent.view', 'organization.dashboard.view',
                                    'organization_user.view']
                },
                {
                    'slug': 'organization_maintainer',
                    'display_name': 'Maintainer',
                    'role_type': 'organization_user',
                    'permissions': ['bot.view', 'bot.add', 'bot.change', 'bot.delete', 'agent.view', 'agent.add',
                                    'agent.change', 'agent.delete', 'organization.dashboard.view',
                                    'organization_user.view', 'organization_user.add', 'organization_user.change',
                                    'organization_user.delete']
                },
                {
                    'slug': 'organization_owner',
                    'display_name': 'Owner',
                    'role_type': 'organization_user',
                    'permissions': ['organization.change', 'organization.delete', 'bot.view', 'bot.add', 'bot.change',
                                    'bot.delete', 'agent.view', 'agent.add', 'agent.change', 'agent.delete',
                                    'organization.dashboard.view', 'organization_user.view',
                                    'organization_user.add', 'organization_user.change', 'organization_user.delete']
                }]

            for role in roles_data:
                role_obj = Role.objects.filter(
                    slug=role['slug'],
                ).first()
                if not role_obj:
                    role_obj = Role.objects.create(
                        slug=role['slug'],
                    )
                role_obj.display_name = role['display_name']
                role_obj.role_type = role['role_type']

                for perm in role['permissions']:
                    permission_role = PermissionRole.objects.filter(
                        role=role_obj,
                        permission=Permission.objects.filter(slug=perm).first()
                    )
                    if not permission_role:
                        PermissionRole.objects.create(
                            role=role_obj,
                            permission=Permission.objects.filter(slug=perm).first()
                        )
                role_obj.save()
