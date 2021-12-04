from authentication.models import User
from django.contrib.auth.models import Permission


def set_user_permession(username, type):
    user = User.objects.get(username=username)
    permissions = Permission.objects.all()
    for permission in permissions:
        if type == 1:
            if permission.codename in ('delete_logentry', 'change_logentry'):
                user.user_permissions.add(permission)
