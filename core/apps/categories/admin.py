from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (
    Category,
    Subcategory,
)


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    prepopulated_fields = {'slug': ('name',)}
