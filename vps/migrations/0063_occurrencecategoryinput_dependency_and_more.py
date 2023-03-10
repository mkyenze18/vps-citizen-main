# Generated by Django 4.0.3 on 2022-12-18 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0062_arrestee_release_date_alter_fingerprints_arrestee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrencecategoryinput',
            name='dependency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dependencies', to='vps.occurrencecategory'),
        ),
        migrations.AddField(
            model_name='occurrencecategoryinput',
            name='dependency_value',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
