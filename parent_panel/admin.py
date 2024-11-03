from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(UserChild)
admin.site.register(History)
admin.site.register(PermittedUser)
admin.site.register(Permission)