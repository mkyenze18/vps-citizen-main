# Generated by Django 4.0.3 on 2022-05-17 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0017_occurrence_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
