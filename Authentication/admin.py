from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import User , Group
from Authentication.models import PublicUsers
from admin_interface.models import Theme



admin.site.unregister(Theme)
admin.site.unregister(User)
admin.site.unregister(Group)
