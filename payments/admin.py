from django.contrib import admin
from .models import Order, OrderItem, Subscription


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Order, OrderAdmin)
admin.site.register(Subscription)
