from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (
    Brand,
    Color,
    Product,
)


class FormModel(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rate', 'brand')
    list_filter = ('category', 'brand', 'rate')
    search_fields = ('name', 'category', 'brand', 'subcategory')


admin.site.register(Brand, ImportExportModelAdmin)
admin.site.register(Color, ImportExportModelAdmin)
admin.site.register(Product, FormModel)
