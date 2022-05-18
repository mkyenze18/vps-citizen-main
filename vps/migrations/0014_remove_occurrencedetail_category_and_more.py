# Generated by Django 4.0.3 on 2022-05-15 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0013_occurrencecategoryinput_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrencedetail',
            name='category',
        ),
        migrations.AddField(
            model_name='occurrencedetail',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vps.occurrencecategory'),
            preserve_default=False,
        ),
    ]