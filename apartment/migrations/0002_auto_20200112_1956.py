# Generated by Django 3.0.2 on 2020-01-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='description',
            field=models.TextField(),
        ),
    ]