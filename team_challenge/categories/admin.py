from django.contrib import admin
from .models import Category, Subcategory
from import_export.admin import ImportExportModelAdmin

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):  
    inlines = [
        SubcategoryInline,
    ]
    prepopulated_fields = {'slug': ('name',)}  