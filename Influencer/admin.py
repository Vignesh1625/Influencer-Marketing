# Influencer/admin.py   
from django.contrib import admin
from django.apps import AppConfig
from .models import InfluencerInfo, InfluencerSocialMedia

@admin.register(InfluencerInfo)
class InfluencerInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'location', 'gender', 'is_verified', 'created_at')
    search_fields = ('full_name', 'location')
    list_filter = ('gender', 'is_verified', 'created_at')

@admin.register(InfluencerSocialMedia)
class InfluencerSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'instagram_handle', 'instagram_followers', 'youtube_channel', 'youtube_subscribers')
    search_fields = ('instagram_handle', 'youtube_channel')
    list_filter = ('created_at',)

    def get_full_name(self, obj):
        try:
            influencer = InfluencerInfo.objects.get(user_id=obj.user_id)
            return influencer.full_name
        except InfluencerInfo.DoesNotExist:
            return "No profile"
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__influencerinfo__full_name'