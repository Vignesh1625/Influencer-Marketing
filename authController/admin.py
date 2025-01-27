# authController/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetOTP, UserSession

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role')
    list_filter = ('role',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role')}
        ),
    )

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