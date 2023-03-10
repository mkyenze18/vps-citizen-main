# Generated by Django 4.0.3 on 2022-06-08 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0018_occurrence_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='ob_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='occurrencedetail',
            name='occurrence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='vps.occurrence'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='occurrence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reporters', to='vps.occurrence'),
        ),
    ]
