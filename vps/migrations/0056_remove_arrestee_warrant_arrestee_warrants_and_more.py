# Generated by Django 4.0.3 on 2022-11-07 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0055_remove_gang_arrestee_arrestee_gangs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrestee',
            name='warrant',
        ),
        migrations.AddField(
            model_name='arrestee',
            name='warrants',
            field=models.ManyToManyField(blank=True, to='vps.warrant_of_arrest'),
        ),
        migrations.AlterField(
            model_name='arrestee',
            name='gangs',
            field=models.ManyToManyField(blank=True, to='vps.gang'),
        ),
        migrations.AlterField(
            model_name='mugshots',
            name='arrestee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mugshots', to='vps.arrestee'),
        ),
    ]
