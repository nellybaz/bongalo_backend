# Generated by Django 3.0.2 on 2020-06-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(max_length=3),
        ),
    ]
