# Generated by Django 4.0.3 on 2022-11-04 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0052_arrestee_date_of_arrest_arrestee_time_of_arrest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrestee',
            name='date_of_arrest',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
