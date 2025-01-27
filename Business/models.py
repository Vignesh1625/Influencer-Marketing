# Business/models.py
from django.db import models
from django.conf import settings
import uuid

class BusinessClient(models.Model):
    """
    Stores business client information with UUID as primary key.
    Linked to the custom User model via ForeignKey.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Business ID'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_client'
    )
    full_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        verbose_name='Gender'
    )
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Client"
        verbose_name_plural = "Business Clients"
        indexes = [
            models.Index(fields=['company_name', 'created_at']),
        ]

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"