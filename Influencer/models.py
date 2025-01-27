# Influencer/models.py
from django.db import models
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class InfluencerInfo(models.Model):
    # Primary key field
    id = models.AutoField(primary_key=True)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='influencer_info'
    )

    full_name = models.CharField(max_length=255)
    bio = models.TextField()
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)  # Add full-text search

    def __str__(self):
        return f"{self.full_name} - {self.location}"

    class Meta:
        verbose_name = "Influencer Information"
        verbose_name_plural = "Influencers Information"
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['location', 'created_at']),
            models.Index(fields=['full_name']),  # Add index for frequently searched field
        ]

class InfluencerSocialMedia(models.Model):
    # Primary key field
    id = models.AutoField(primary_key=True)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_media'
    )

    instagram_handle = models.CharField(max_length=255, blank=True, null=True)
    instagram_followers = models.PositiveIntegerField(default=0)
    youtube_channel = models.CharField(max_length=255, blank=True, null=True)
    youtube_subscribers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.influencerinfo.full_name}'s Social Media"

    class Meta:
        verbose_name = "Social Media Account"
        verbose_name_plural = "Social Media Accounts"