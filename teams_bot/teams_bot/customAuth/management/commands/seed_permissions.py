from django.db import transaction
from django.core.management.base import BaseCommand
from customAuth.models.model_permissions import Permission


class Command(BaseCommand):
    help = 'seed permissions'

    def handle(self, *args, **options):
        with transaction.atomic():
            permissions_data = [
                {'slug': 'organization_user.view', 'display_name': 'organization User View'},
                {'slug': 'organization_user.add', 'display_name': 'organization User Add'},
                {'slug': 'organization_user.change', 'display_name': 'organization User Change'},
                {'slug': 'organization_user.delete', 'display_name': 'organization User Delete'},

                {'slug': 'organization.view', 'display_name': 'organization View'},
                {'slug': 'organization.add', 'display_name': 'organization Add'},
                {'slug': 'organization.change', 'display_name': 'organization Change'},
                {'slug': 'organization.delete', 'display_name': 'organization Delete'},

                {'slug': 'agent.add', 'display_name': 'Agent Add'},
                {'slug': 'agent.change', 'display_name': 'Agent Change'},
                {'slug': 'agent.delete', 'display_name': 'Agent Delete'},
                {'slug': 'agent.view', 'display_name': 'Agent View'},

                {'slug': 'bot.add', 'display_name': 'Bot Add'},
                {'slug': 'bot.change', 'display_name': 'Bot Change'},
                {'slug': 'bot.delete', 'display_name': 'Bot Delete'},
                {'slug': 'bot.view', 'display_name': 'Bot View'},

                {'slug': 'organization.dashboard.view', 'display_name': 'organization Dashboard View'},
            ]

            for perm in permissions_data:
                permission = Permission.objects.filter(slug=perm['slug']).first()
                if not permission:
                    permission = Permission.objects.create(
                        slug=perm['slug'],
                    )
                permission.display_name = perm['display_name']
                permission.save()
