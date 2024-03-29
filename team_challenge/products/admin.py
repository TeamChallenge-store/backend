from django.contrib import admin
from .models import Brand, Color, Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Brand, ImportExportModelAdmin)
admin.site.register(Color, ImportExportModelAdmin)
admin.site.register(Product, ImportExportModelAdmin)