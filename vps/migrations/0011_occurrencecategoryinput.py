# Generated by Django 4.0.3 on 2022-05-14 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0010_alter_policeofficer_mug_shot'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccurrenceCategoryInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('choices', models.TextField()),
                ('occurrence_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vps.occurrencecategory')),
            ],
        ),
    ]
