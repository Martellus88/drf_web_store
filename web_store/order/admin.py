from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'first_name', 'last_name',
                    'email', 'phone', 'address', 'city', 'created_at', 'paid')
    inlines = [OrderItemAdmin]
