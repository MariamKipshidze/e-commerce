from django.contrib import admin

from store.models import Product
from store.models import ProductCollection
from store.models import Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category']
    search_fields = ['name']
    list_filter = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['name']
    list_filter = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    prepopulated_fields = {
        'slug': ['title']
    }
