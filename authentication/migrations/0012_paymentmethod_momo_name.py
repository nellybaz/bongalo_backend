# Generated by Django 3.0.2 on 2020-05-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20200523_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='momo_name',
            field=models.CharField(default='', max_length=20),
        ),
    ]