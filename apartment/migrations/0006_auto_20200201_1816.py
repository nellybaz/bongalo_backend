# Generated by Django 3.0.2 on 2020-02-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0005_auto_20200201_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activebooking',
            name='check_in',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='activebooking',
            name='check_out',
            field=models.TimeField(),
        ),
    ]