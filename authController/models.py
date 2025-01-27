# authController/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """Custom user manager handling UUID as primary key"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Unique ID'
    )
    ROLE_CHOICES = (
        ('BUSINESS', 'Business'),
        ('INFLUENCER', 'Influencer'),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name='User Role'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']

class UserSession(models.Model):
    """Stores authenticated sessions with CSRF tokens"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        db_index=True
    )
    session_id = models.CharField(max_length=40, unique=True, db_index=True)
    csrf_token = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['session_id', 'csrf_token']),
            models.Index(fields=['expires_at']),
        ]

    def is_valid(self):
        return timezone.now() < self.expires_at

    @classmethod
    def clean_expired_sessions(cls):
        """Class method to clean up expired sessions"""
        cls.objects.filter(expires_at__lt=timezone.now()).delete()

    def save(self, *args, **kwargs):
        # Clean up expired sessions before saving new one
        UserSession.clean_expired_sessions()
        super().save(*args, **kwargs)

class PasswordResetOTP(models.Model):
    """UUID-based password reset tokens"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reset_otps',
        db_index=True
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at