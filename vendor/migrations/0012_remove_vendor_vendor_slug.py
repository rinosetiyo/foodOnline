# Generated by Django 4.1.7 on 2024-01-02 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0011_alter_vendor_vendor_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_slug',
        ),
    ]
