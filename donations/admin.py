from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'food_name',
        'donor',
        'category',
        'quantity',
        'unit',
        'city',
        'status',
        'expiry_at',
        'created_at'
    )
    list_filter = ('status', 'category', 'city', 'created_at')
    search_fields = ('food_name', 'donor__username', 'donor__email', 'pickup_address', 'city', 'description')
    prepopulated_fields = {'slug': ('food_name',)}
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = ['mark_as_available', 'mark_as_expired']

    @admin.action(description="Mark selected donations as Available")
    def mark_as_available(self, request, queryset):
        updated = queryset.update(status='AVAILABLE')
        self.message_user(request, f"{updated} donations marked as Available.")

    @admin.action(description="Mark selected donations as Expired")
    def mark_as_expired(self, request, queryset):
        updated = queryset.update(status='EXPIRED')
        self.message_user(request, f"{updated} donations marked as Expired.")
