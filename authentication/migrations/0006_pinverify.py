# Generated by Django 3.0.2 on 2020-03-09 07:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_userprofile_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PinVerify',
            fields=[
                ('uuid',
                 models.CharField(
                     default=uuid.uuid4,
                     max_length=100,
                     primary_key=True,
                     serialize=False,
                     unique=True)),
                ('pin',
                 models.CharField(
                     max_length=10)),
                ('user',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='authentication.UserProfile')),
            ],
        ),
    ]
