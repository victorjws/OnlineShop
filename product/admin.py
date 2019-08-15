from django.contrib import admin

from .models import Review
from .models import Product
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    readonly_fields = ('register_date',)


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
