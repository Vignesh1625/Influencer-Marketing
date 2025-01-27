# Generated by Django 5.1.1 on 2025-01-27 12:25

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('base_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('location', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'verbose_name': 'Influencer Information',
                'verbose_name_plural': 'Influencers Information',
            },
        ),
        migrations.CreateModel(
            name='InfluencerSocialMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('instagram_handle', models.CharField(blank=True, max_length=255, null=True)),
                ('instagram_followers', models.PositiveIntegerField(default=0)),
                ('youtube_channel', models.CharField(blank=True, max_length=255, null=True)),
                ('youtube_subscribers', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Social Media Account',
                'verbose_name_plural': 'Social Media Accounts',
            },
        ),
    ]
