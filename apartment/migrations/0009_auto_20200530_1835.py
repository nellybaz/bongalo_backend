# Generated by Django 3.0.2 on 2020-05-30 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0008_auto_20200407_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activebooking',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='activebooking',
            name='check_out',
        ),
    ]
