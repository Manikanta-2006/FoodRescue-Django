from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Details'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_organization', 'is_staff')
    list_select_related = ('profile',)

    def get_role(self, instance):
        return instance.profile.role if hasattr(instance, 'profile') else '-'
    get_role.short_description = 'Role'

    def get_organization(self, instance):
        return instance.profile.organization_name if hasattr(instance, 'profile') else '-'
    get_organization.short_description = 'Organization'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'organization_name', 'phone', 'city', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'organization_name', 'phone', 'address', 'city')
    ordering = ('-created_at',)
    actions = ['verify_selected_ngos', 'unverify_selected_ngos']

    @admin.action(description="Verify selected NGOs and organizations")
    def verify_selected_ngos(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f"{count} organization profiles were successfully verified.")

    @admin.action(description="Revoke verification for selected profiles")
    def unverify_selected_ngos(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f"{count} profiles had their verification status revoked.")
