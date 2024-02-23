from django.contrib import admin
from .models import Category, Subcategory

class SubcategoryInline(admin.TabularInline):
    model = Subcategory

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]

admin.site.register(Category, CategoryAdmin)
