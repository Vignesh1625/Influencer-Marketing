# authController/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetOTP, UserSession

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the User model.
    """
    list_display = ('email', 'role', 'created_at', 'is_staff')
    list_filter = ('role', 'is_staff', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at',)

class PasswordResetOTPAdmin(admin.ModelAdmin):
    """
    Admin interface for the PasswordResetOTP model.
    """
    list_display = ('user_email', 'otp', 'created_at', 'expires_at', 'is_valid')
    readonly_fields = ('created_at', 'expires_at')
    search_fields = ('user__email', 'otp')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(PasswordResetOTP, PasswordResetOTPAdmin)
admin.site.register(UserSession)