from django.contrib import admin

from .models import Cart
from .models import Order


class CartAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
