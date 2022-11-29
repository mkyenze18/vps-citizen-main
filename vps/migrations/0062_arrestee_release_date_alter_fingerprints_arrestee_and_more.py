# Generated by Django 4.0.3 on 2022-11-29 22:58

from django.db import migrations, models
import django.db.models.deletion
import helpers.upload_file_name


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0061_fingerprints_police_station_fingerprints_posted_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrestee',
            name='release_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='arrestee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fingerprints', to='vps.arrestee'),
        ),
        migrations.AlterField(
            model_name='mugshots',
            name='front_view',
            field=models.ImageField(blank=True, upload_to=helpers.upload_file_name.arrestee_mugshot_directory_path),
        ),
        migrations.AlterField(
            model_name='mugshots',
            name='left_view',
            field=models.ImageField(blank=True, upload_to=helpers.upload_file_name.arrestee_mugshot_directory_path),
        ),
        migrations.AlterField(
            model_name='mugshots',
            name='right_view',
            field=models.ImageField(blank=True, upload_to=helpers.upload_file_name.arrestee_mugshot_directory_path),
        ),
    ]
