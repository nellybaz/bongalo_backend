# Generated by Django 3.0.2 on 2020-03-08 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20200308_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.UserProfile'),
        ),
    ]