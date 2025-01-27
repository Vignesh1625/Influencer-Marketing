# products/models.py
from django.db import models
from Business.models import BusinessClient
from Influencer.models import InfluencerInfo
from datetime import timedelta

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(
        BusinessClient, 
        on_delete=models.CASCADE, 
        related_name='products',
        db_index=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    status = models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status'])
        ]

    def __str__(self):
        return f"{self.name} ({self.business})"


#accepted - Influencer has accepted the request
class ProductInfluencer(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='requests', db_index=True)
    influencer = models.ForeignKey(
        InfluencerInfo, 
        on_delete=models.CASCADE,
        related_name='collaborations',
        to_field='user_id'  # Reference the user_id field
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    class Meta:
        unique_together = ('product', 'influencer')
        indexes = [
            models.Index(fields=['request_date']),
        ]   

    def __str__(self):
        return f"{self.product} - {self.influencer} ({self.status})"
    

#pending and new matches - Influencer has not accepted the request
class NewMatches(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='new_matches')
    influencer = models.ForeignKey(
        InfluencerInfo, 
        on_delete=models.CASCADE,
        related_name='new_matches',
        to_field='user_id'  # Reference the user_id field
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') 

    created_at = models.DateTimeField(auto_now_add=True)
    auto_delete_at = models.DateTimeField()

    class Meta:
        unique_together = ('product', 'influencer')
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product} - {self.influencer}"

    def save(self, *args, **kwargs):
        if not self.auto_delete_at:
            self.auto_delete_at = self.created_at + timedelta(days=30)
        super().save(*args, **kwargs)

    def clean(self):
        # Validate that an influencer isn't already matched
        if NewMatches.objects.filter(
            product=self.product,
            influencer=self.influencer,
            status='pending'
        ).exists():
            raise ValidationError('This match already exists')