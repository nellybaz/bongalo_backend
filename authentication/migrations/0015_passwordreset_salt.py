# Generated by Django 3.0.2 on 2020-06-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_auto_20200628_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordreset',
            name='salt',
            field=models.CharField(default='234', max_length=225),
            preserve_default=False,
        ),
    ]
