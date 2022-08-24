# Generated by Django 4.0.3 on 2022-07-01 22:29

from django.db import migrations, models
import helpers.upload_file_name


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0027_rename_evidence_item_evidenceitemimage_evidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidenceitemimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=helpers.upload_file_name.evidence_image_directory_path),
        ),
    ]