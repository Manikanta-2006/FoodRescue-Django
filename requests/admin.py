from django.contrib import admin
from .models import FoodRequest, Delivery


@admin.register(FoodRequest)
class FoodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'donation',
        'receiver',
        'quantity_requested',
        'status',
        'requested_at'
    )
    list_filter = ('status', 'requested_at')
    search_fields = ('donation__food_name', 'receiver__username', 'receiver__profile__organization_name', 'message')
    ordering = ('-requested_at',)
    date_hierarchy = 'requested_at'


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'food_request',
        'volunteer',
        'delivery_status',
        'pickup_time',
        'delivery_time',
        'created_at'
    )
    list_filter = ('delivery_status', 'created_at')
    search_fields = (
        'food_request__donation__food_name',
        'volunteer__username',
        'volunteer__first_name',
        'volunteer__last_name',
        'remarks'
    )
    ordering = ('-created_at',)
    actions = ['mark_as_delivered']

    @admin.action(description="Mark selected deliveries as Delivered")
    def mark_as_delivered(self, request, queryset):
        for delivery in queryset:
            delivery.mark_delivered(remarks="Marked as delivered via Admin Action")
        self.message_user(request, f"{queryset.count()} deliveries updated to Delivered.")
