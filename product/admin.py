from django.contrib import admin

from .models import Product
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    readonly_fields = ('register_date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
