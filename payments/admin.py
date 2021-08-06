from django.contrib import admin
from .models import Order, OrderItem, Subscription


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Order, OrderAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'removed_at']

admin.site.register(Subscription, SubscriptionAdmin)
