# Generated by Django 4.0.3 on 2022-08-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0034_occurrencecounter_alter_reporter_email_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=20)),
                ('longitude', models.CharField(max_length=20)),
            ],
        ),
    ]
