from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Order, OrderAdmin)
