from django.contrib import admin
from .models import Brand, Color, Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Product, ImportExportModelAdmin)