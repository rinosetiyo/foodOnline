# Generated by Django 4.1.7 on 2024-01-02 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_rename_vendor_slug_vendor_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='slug',
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
