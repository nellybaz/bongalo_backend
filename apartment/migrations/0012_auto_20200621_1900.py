# Generated by Django 3.0.2 on 2020-06-21 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0011_auto_20200530_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='extras',
            field=models.TextField(blank=True, default=''),
        ),
    ]
