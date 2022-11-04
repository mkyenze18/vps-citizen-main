# Generated by Django 4.0.3 on 2022-11-04 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0054_alter_next_of_kin_arrestee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gang',
            name='arrestee',
        ),
        migrations.AddField(
            model_name='arrestee',
            name='gangs',
            field=models.ManyToManyField(to='vps.gang'),
        ),
        migrations.AlterField(
            model_name='accomplice',
            name='arrestee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accomplices', to='vps.arrestee'),
        ),
    ]
