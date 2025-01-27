# Generated by Django 5.1.1 on 2025-01-27 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Business', '0001_initial'),
        ('Influencer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='Business.businessclient')),
            ],
        ),
        migrations.CreateModel(
            name='NewMatches',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auto_delete_at', models.DateTimeField()),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_matches', to='Influencer.influencerinfo', to_field='user_id')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_matches', to='Products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfluencer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to='Influencer.influencerinfo', to_field='user_id')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='Products.product')),
            ],
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='Products_pr_name_525943_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_at'], name='Products_pr_created_08b84c_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['status'], name='Products_pr_status_aa528e_idx'),
        ),
        migrations.AddIndex(
            model_name='newmatches',
            index=models.Index(fields=['created_at'], name='Products_ne_created_386e3f_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='newmatches',
            unique_together={('product', 'influencer')},
        ),
        migrations.AddIndex(
            model_name='productinfluencer',
            index=models.Index(fields=['request_date'], name='Products_pr_request_e45134_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productinfluencer',
            unique_together={('product', 'influencer')},
        ),
    ]
