from django.contrib import admin
from .models import Order, User
from import_export.admin import ImportExportModelAdmin

admin.site.register(User)
admin.site.register(Order)
