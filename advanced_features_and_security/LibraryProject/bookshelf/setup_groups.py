from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        permissions = {
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
            "Editors": ["can_create", "can_edit"],
            "Viewers": ["can_view"],
        }

        for group_name, perms in permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm in perms:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Groups and permissions created successfully."))
