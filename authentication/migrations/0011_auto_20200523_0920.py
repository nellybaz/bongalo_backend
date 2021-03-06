# Generated by Django 3.0.2 on 2020-05-23 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_userprofile_verification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='account_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='account_number',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='bank_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='swift_code',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='momo_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
