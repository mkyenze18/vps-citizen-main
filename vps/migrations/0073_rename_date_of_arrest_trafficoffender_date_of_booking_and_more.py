# Generated by Django 4.0.3 on 2023-01-18 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0072_trafficoffender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trafficoffender',
            old_name='date_of_arrest',
            new_name='date_of_booking',
        ),
        migrations.RenameField(
            model_name='trafficoffender',
            old_name='time_of_arrest',
            new_name='time_of_booking',
        ),
    ]
