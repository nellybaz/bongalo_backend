# Generated by Django 3.0.2 on 2020-02-24 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20200131_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_host',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
