# Generated by Django 5.1.1 on 2025-01-27 12:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Business', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='businessclient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business_client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='businessclient',
            index=models.Index(fields=['company_name', 'created_at'], name='Business_bu_company_7e598a_idx'),
        ),
    ]
