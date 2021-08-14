from django.contrib import admin
# from .models import Order, OrderItem, Subscription


# class OrderItemAdmin(admin.StackedInline):
#     model = OrderItem


# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemAdmin]
#     list_display = ['user', 'stripe_payment_intent_id', 'total_price', 'created_at']
#     readonly_fields = ['created_at']
    
#     def has_change_permission(self, request, obj=None):
#         # make all fields read only
#         return False


# admin.site.register(Order, OrderAdmin)


# class SubscriptionAdmin(admin.ModelAdmin):
#     list_display = ['email', 'stripe_subscription_id', 'active']
#     readonly_fields = ['created_at']
    
#     def has_change_permission(self, request, obj=None):
#         # make all fields read only
#         return False

# admin.site.register(Subscription, SubscriptionAdmin)
