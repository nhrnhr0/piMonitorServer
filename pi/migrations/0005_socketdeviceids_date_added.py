# Generated by Django 4.0 on 2023-03-07 00:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pi', '0004_socketdeviceids'),
    ]

    operations = [
        migrations.AddField(
            model_name='socketdeviceids',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
