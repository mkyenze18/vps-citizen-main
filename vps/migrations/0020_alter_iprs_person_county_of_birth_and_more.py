# Generated by Django 4.0.3 on 2022-06-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0019_occurrence_ob_no_alter_occurrencedetail_occurrence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iprs_person',
            name='county_of_birth',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='iprs_person',
            name='district_of_birth',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='iprs_person',
            name='division_of_birth',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='iprs_person',
            name='location_of_birth',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
