# Product/admin.py
from django.contrib import admin
from .models import Product, ProductInfluencer, NewMatches

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'business__company_name')
    date_hierarchy = 'created_at'

@admin.register(ProductInfluencer)
class ProductInfluencerAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'influencer', 'request_date')
    list_filter = ('request_date',)
    search_fields = ('product__name', 'influencer__full_name')

@admin.register(NewMatches)
class NewMatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'influencer', 'status', 'created_at', 'auto_delete_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'influencer__full_name')
    date_hierarchy = 'created_at'
