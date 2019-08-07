from django.contrib import admin

from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    readonly_fields = ('register_date',)


admin.site.register(Product, ProductAdmin)
