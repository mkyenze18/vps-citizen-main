# Generated by Django 4.0.3 on 2022-07-21 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0029_vehicle_trafficoffender_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='trafficoffender',
            name='Vehicle',
        ),
        migrations.CreateModel(
            name='TrafficOccurrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vps.vehicle')),
                ('occurrence', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vps.occurrence')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.BooleanField(default=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vps.permissionmodule')),
            ],
        ),
        migrations.AddField(
            model_name='trafficoffender',
            name='offence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='vps.trafficoccurrence'),
        ),
    ]
