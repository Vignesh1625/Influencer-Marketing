# Generated by Django 5.1.1 on 2025-01-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0003_delete_usersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessclient',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
