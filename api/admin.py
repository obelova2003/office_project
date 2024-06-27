from django.contrib import admin

from .models import OfficeUser, Report, Application, Storage

admin.site.register(OfficeUser)
admin.site.register(Report)
admin.site.register(Application)
admin.site.register(Storage)
