from django.contrib import admin

from customer.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'register_date')
    readonly_fields = ('register_date',)


admin.site.register(Customer, CustomerAdmin)
