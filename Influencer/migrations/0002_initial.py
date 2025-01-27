# Generated by Django 5.1.1 on 2025-01-27 12:25

import django.contrib.postgres.indexes
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Influencer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='influencerinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='influencer_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='influencersocialmedia',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='influencerinfo',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='Influencer__search__e8934a_gin'),
        ),
        migrations.AddIndex(
            model_name='influencerinfo',
            index=models.Index(fields=['location', 'created_at'], name='Influencer__locatio_76aa0a_idx'),
        ),
        migrations.AddIndex(
            model_name='influencerinfo',
            index=models.Index(fields=['full_name'], name='Influencer__full_na_8ad5a3_idx'),
        ),
    ]
