# Business/admin.py
from django.contrib import admin
from .models import BusinessClient

@admin.register(BusinessClient)
class BusinessClientAdmin(admin.ModelAdmin):
    """
    Admin interface for the BusinessClient model.
    """
    list_display = ('full_name', 'company_name', 'location', 'created_at')
    list_filter = ('created_at', 'location')
    search_fields = ('full_name', 'company_name', 'location')
    readonly_fields = ('id', 'created_at')

    def get_queryset(self, request):
        """
        Optimize database queries by selecting related User objects.
        """
        return super().get_queryset(request).select_related('user')

