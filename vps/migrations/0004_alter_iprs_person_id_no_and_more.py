# Generated by Django 4.0.3 on 2022-04-06 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0003_gender_alter_iprs_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iprs_person',
            name='id_no',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='iprs_person',
            name='passport_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
