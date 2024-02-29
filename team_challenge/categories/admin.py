from django.contrib import admin
from .models import Category, Subcategory

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    prepopulated_fields = {'slug': ('name',)} 

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    prepopulated_fields = {'slug': ('name',)}  

admin.site.register(Category, CategoryAdmin)